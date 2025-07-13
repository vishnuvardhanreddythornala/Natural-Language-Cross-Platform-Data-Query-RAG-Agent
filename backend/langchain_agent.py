import os
import pandas as pd
import re
from pymongo import MongoClient
import mysql.connector
from langchain_groq import ChatGroq
from langchain_experimental.agents.agent_toolkits.pandas.base import create_pandas_dataframe_agent
from dotenv import load_dotenv
import json

import ast
from collections import defaultdict

# Load environment variables
load_dotenv()

# Constants
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
OPENAI_API_KEY = os.getenv("GROQ_API_KEY")
DB_NAME = "wealth_portfolio"

# Aggregate helper (if required in future)
def aggregate_portfolio_values(data):
    aggregated = defaultdict(float)
    for k, v in data.items():
        aggregated[k] += v
    return dict(aggregated)

# Safe eval utility (unused here but useful for expression parsing)
def safe_eval(expr):
    try:
        node = ast.parse(expr, mode='eval')
        if all(isinstance(n, (ast.Expression, ast.BinOp, ast.Num, ast.Add, ast.Sub, ast.Mult, ast.Div)) for n in ast.walk(node)):
            return eval(expr)
        else:
            raise ValueError("Unsafe expression")
    except:
        return expr

# Load data from MongoDB and MySQL, merge for single dataframe
def load_data():
    # ➔ MongoDB
    client = MongoClient(MONGO_URI)
    mongo_db = client[DB_NAME]
    client_profiles = list(mongo_db.client_profiles.find())
    clients_df = pd.DataFrame(client_profiles)
    if "_id" in clients_df.columns:
        clients_df.drop(columns=["_id"], inplace=True)

    # ➔ MySQL
    sql_conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Login@630",
        database=DB_NAME
    )
    cursor = sql_conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM transactions")
    transactions = cursor.fetchall()
    transactions_df = pd.DataFrame(transactions)

    # ➔ Merge (ALL CLIENTS LEFT JOIN)
    merged_df = pd.merge(clients_df, transactions_df, on="client_name", how="left")
    merged_df.fillna("", inplace=True)

    # ➔ Replace missing transaction value with 0 for aggregation queries
    merged_df["value"] = pd.to_numeric(merged_df["value"], errors="coerce").fillna(0)

    # ➔ Convert list columns to comma-separated strings for LLM readability
    for col in merged_df.columns:
        if merged_df[col].apply(type).eq(list).any():
            merged_df[col] = merged_df[col].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)

    return merged_df.drop_duplicates()

# LLM setup
llm = ChatGroq(
    api_key=OPENAI_API_KEY,
    model="llama3-8b-8192",
    temperature=0
)

# General instruction for business queries
GENERAL_INSTRUCTION = (
    "You are a professional wealth portfolio data analyst. "
    "Answer the user's business question using the dataframe provided. "
    "You can use pandas dataframe operations like groupby, sum, max, etc. "
    "For questions about top portfolios, group by client_name and sum their values. "
    "For breakup per relationship manager, group by relationship_manager and sum their values. "
    "For top relationship managers, rank by total portfolio value handled. "
    "For highest holders of specific stocks, filter by stock_name and sort by value descending. "
    "When the user mentions crore, interpret 1 crore as 10,000,000. "
    "Return ONLY the final answer in valid JSON format where each key is the client or entity name "
    "and each value is the numeric portfolio value. "
    "For stock-specific questions, include the stock name in the key for clarity, for example: "
    "{\"Virat Kohli - Infosys\": 23000000.00, \"KL Rahul - Infosys\": 15000000.00}. "
    "Do NOT return explanations or comments. Only return the JSON dictionary mapping."
)


# Main query runner
def run_query(query: str) -> dict:
    try:
        merged_df = load_data()
        print(" Clients in merged_df:", merged_df["client_name"].unique())
        print(" Total unique clients:", merged_df["client_name"].nunique())
        print(" Clients with no transactions:", merged_df.loc[merged_df["value"] == 0, "client_name"].tolist())

        agent = create_pandas_dataframe_agent(
            llm,
            merged_df,
            verbose=True,
            allow_dangerous_code=True,
        )

        q_lower = query.lower()

        # ➔ Hardcoded logic for top five portfolios
        if "top five portfolios" in q_lower or "top 5 portfolios" in q_lower:
            df_sum = merged_df.groupby('client_name')['value'].sum().sort_values(ascending=False).head(5)
            result_dict = df_sum.to_dict()

            graph_data = [{"label": k, "value": v} for k, v in result_dict.items()]
            table_data = [{"client": k, "portfolio_value": v} for k, v in result_dict.items()]

            return {
                "text": f"The top five portfolios (by total investment value) are: {result_dict}",
                "graph": graph_data,
                "table": table_data
            }

        # ➔ Hardcoded logic for total investments per client
        if "total investments per client" in q_lower:
            df_sum = merged_df.groupby('client_name')['value'].sum()
            result_dict = df_sum.to_dict()

            graph_data = [{"label": k, "value": v} for k, v in result_dict.items()]
            table_data = [{"client": k, "portfolio_value": v} for k, v in result_dict.items()]

            return {
                "text": f"Total investments per client:\n{result_dict}",
                "graph": graph_data,
                "table": table_data
            }

        # ➔ Hardcoded logic for highest holders of specific stock
        if "highest holders" in q_lower and "stock" in q_lower:
            
            match = re.search(r"of\s+(.*?)(\?|$)", query, re.IGNORECASE)
            if match:
                stock = match.group(1).strip()
                
                if stock.lower().endswith(" stock"):
                    stock = stock[:-6].strip()


                # Filter and group
                df_filtered = merged_df[merged_df["stock_name"].str.lower() == stock.lower()]

                if df_filtered.empty:
                    return {
                        "text": f"No holdings found for stock '{stock}'.",
                        "graph": [],
                        "table": []
                    }

                df_grouped = df_filtered.groupby("client_name")["value"].sum().sort_values(ascending=False)
                result_dict = df_grouped.to_dict()

                graph_data = [{"label": k, "value": v} for k, v in result_dict.items()]
                table_data = [{"client": k, "portfolio_value": v} for k, v in result_dict.items()]

                return {
                    "text": f"Highest holders of {stock}:\n{result_dict}",
                    "graph": graph_data,
                    "table": table_data
                }

        # ➔ For all other queries, route to LLM agent with business instructions
        full_query = f"{GENERAL_INSTRUCTION}\n\nQuestion: {query}"

        result = agent.run(full_query)
        print(" Raw result from LLM:", result)

        # ➔ Parse JSON dictionary from LLM result
        match = re.search(r"{.*}", result, re.DOTALL)
        if match:
            try:
                parsed = json.loads(match.group())

                # ➔ Convert if result is a column-based dict
                if isinstance(parsed, dict) and "client_name" in parsed and "value" in parsed:
                    result_dict = dict(zip(parsed["client_name"], map(float, parsed["value"])))
                else:
                    result_dict = parsed

                graph_data = [{"label": k, "value": v} for k, v in result_dict.items()]
                table_data = [{"client": k, "portfolio_value": v} for k, v in result_dict.items()]
                summary_text = "\n".join([f"{k}: {v}" for k, v in result_dict.items()])

                return {
                    "text": f"Here is your result:\n{summary_text}",
                    "graph": graph_data,
                    "table": table_data
                }

            except Exception as e:
                print("⚠️ JSON parse failed:", e)

        # ➔ If result is plain text (no JSON), return consistent empty graph/table
        return {
            "text": result if isinstance(result, str) else str(result),
            "graph": [],
            "table": []
        }

    except Exception as e:
        return {
            "text": f" Error: {str(e)}",
            "graph": [],
            "table": []
        }

