from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
from langchain_agent import run_query
from pymongo import MongoClient
import mysql.connector
import os
from datetime import datetime
import csv
from io import StringIO

#  Load environment variables
load_dotenv()

app = FastAPI()

#  MongoDB setup
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
mongo_client = MongoClient(MONGO_URI)
mongo_db = mongo_client["wealth_portfolio"]
queries_collection = mongo_db["recent_queries"]

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#  Root test endpoint
@app.get("/")
def read_root():
    return {"message": " Valuefy RAG Backend is Running 🚀"}

# Handle Query & Store in MongoDB
@app.post("/query")
async def handle_query(request: Request):
    data = await request.json()
    question = data.get("question", "")

    if not question:
        return {"error": "No question provided"}

    result = run_query(question)

    timestamp = datetime.now().strftime("%d-%b %I:%M %p")
    queries_collection.insert_one({"text": question, "time": timestamp})

    return {
        "response": result.get("text", ""),
        "graph_data": result.get("graph", []),
        "table_data": result.get("table", [])
    }

# Get all client profiles
@app.get("/clients")
def get_all_clients():
    clients = list(mongo_db["client_profiles"].find({}, {"_id": 0}))
    return {"clients": clients}

# Get clients by risk appetite
@app.get("/clients/risk/{risk_level}")
def get_clients_by_risk(risk_level: str):
    clients = list(mongo_db["client_profiles"].find({"risk_appetite": risk_level.capitalize()}, {"_id": 0}))
    return {"clients": clients}

# Get clients by investment preference
@app.get("/clients/preference/{preference}")
def get_clients_by_preference(preference: str):
    clients = list(mongo_db["client_profiles"].find({"investment_preferences": preference}, {"_id": 0}))
    return {"clients": clients}

# Get all recent queries
@app.get("/recent-queries")
def get_recent_queries():
    queries = list(queries_collection.find({}, {"_id": 0}).sort("_id", -1))
    return {"queries": queries}

#  Delete specific query by index
@app.delete("/recent-queries/{index}")
def delete_recent_query(index: int):
    try:
        queries = list(queries_collection.find().sort("_id", -1))
        if 0 <= index < len(queries):
            to_delete = queries[index]
            queries_collection.delete_one({"_id": to_delete["_id"]})
            return {"message": "Deleted", "deleted": {"text": to_delete["text"], "time": to_delete["time"]}}
        else:
            raise HTTPException(status_code=404, detail="Query not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#  Clear all recent queries
@app.delete("/recent-queries/clear")
def clear_recent_queries():
    result = queries_collection.delete_many({})
    return {"message": f"Deleted {result.deleted_count} queries"}

# Export recent queries as CSV
@app.get("/recent-queries/export")
def export_recent_queries():
    queries = list(queries_collection.find({}, {"_id": 0}).sort("_id", -1))
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["Query", "Timestamp"])
    for q in queries:
        writer.writerow([q.get("text", ""), q.get("time", "")])
    output.seek(0)
    return StreamingResponse(output, media_type="text/csv", headers={
        "Content-Disposition": "attachment; filename=recent_queries.csv"
    })

# Filter recent queries by date range
@app.get("/recent-queries/filter")
def filter_recent_queries(start: str = Query(...), end: str = Query(...)):
    try:
        start_date = datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.strptime(end, "%Y-%m-%d")
        all_queries = list(queries_collection.find().sort("_id", -1))
        filtered = [
            q for q in all_queries
            if start_date <= datetime.strptime(q["time"], "%d-%b %I:%M %p") <= end_date
        ]
        return {"queries": filtered}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Date parsing error: {str(e)}")

# Dashboard metrics with real charts data
@app.get("/dashboard-metrics")
def get_dashboard_metrics():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Login@630",
            database="wealth_portfolio"
        )
        cursor = conn.cursor(dictionary=True)

        # ➔ Stats
        cursor.execute("SELECT SUM(value) AS total_aum FROM transactions")
        total_aum = cursor.fetchone()["total_aum"] or 0

        cursor.execute("SELECT COUNT(DISTINCT relationship_manager) AS active_rms FROM transactions")
        active_rms = cursor.fetchone()["active_rms"] or 0

        cursor.execute("SELECT COUNT(*) AS high_risk FROM transactions WHERE value > 100000")
        high_risk = cursor.fetchone()["high_risk"] or 0

        cursor.execute("SELECT COUNT(DISTINCT client_name) AS top_portfolios FROM transactions")
        top_portfolios = cursor.fetchone()["top_portfolios"] or 0

        # ➔ Portfolio growth (month-wise aggregation)
        cursor.execute("""
            SELECT DATE_FORMAT(transaction_date, '%Y-%m') AS month, SUM(value) AS total
            FROM transactions
            GROUP BY month
            ORDER BY month
        """)
        growth_rows = cursor.fetchall()
        portfolio_growth = [{"month": row["month"], "value": float(row["total"])} for row in growth_rows]

        # ➔ Asset allocation (percent per stock)
        cursor.execute("""
            SELECT stock_name, SUM(value) AS total
            FROM transactions
            GROUP BY stock_name
        """)
        asset_rows = cursor.fetchall()
        grand_total = sum(row["total"] for row in asset_rows) or 1  # avoid division by zero
        asset_allocation = [
            {"asset": row["stock_name"], "percent": round(row["total"] * 100 / grand_total, 2)}
            for row in asset_rows
        ]

        # ➔ Top RMs with clients managed
        cursor.execute("""
            SELECT relationship_manager, COUNT(*) as clients
            FROM transactions
            GROUP BY relationship_manager
        """)
        rms = cursor.fetchall()
        rm_clients = [{"rm": r["relationship_manager"], "clients": r["clients"]} for r in rms]

        cursor.close()
        conn.close()

        return {
            "top_portfolios": int(top_portfolios),
            "total_aum": f"₹{float(total_aum):,.0f}",
            "active_rms": int(active_rms),
            "high_risk": int(high_risk),
            "portfolio_growth": portfolio_growth,
            "asset_allocation": asset_allocation,
            "rm_clients": rm_clients,
        }

    except Exception as e:
        return {"error": str(e)}
