from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["wealth_portfolio"]
collection = db["client_profiles"]

# Clear previous data for a fresh insert (optional)
collection.delete_many({})

# Realistic client profiles
clients = [
    {
        "client_name": "Virat Kohli",
        "risk_appetite": "High",
        "investment_preferences": ["Equity", "Real Estate", "Startups"],
        "relationship_manager": "Neha Shah",
        "address": "Delhi"
    },
    {
        "client_name": "Aamir Khan",
        "risk_appetite": "Medium",
        "investment_preferences": ["Mutual Funds", "Bonds"],
        "relationship_manager": "Rajesh Mehta",
        "address": "Mumbai"
    },
    {
        "client_name": "MS Dhoni",
        "risk_appetite": "High",
        "investment_preferences": ["Equity", "AgriTech", "Real Estate"],
        "relationship_manager": "Ravi Mehra",
        "address": "Ranchi"
    },
    {
        "client_name": "Alia Bhatt",
        "risk_appetite": "Medium",
        "investment_preferences": ["ESG Funds", "Startups"],
        "relationship_manager": "Sneha Kapoor",
        "address": "Mumbai"
    },
    {
        "client_name": "Rohit Sharma",
        "risk_appetite": "High",
        "investment_preferences": ["Crypto", "Equity"],
        "relationship_manager": "Ankit Verma",
        "address": "Nagpur"
    },
    {
        "client_name": "Deepika Padukone",
        "risk_appetite": "Low",
        "investment_preferences": ["PPF", "Real Estate"],
        "relationship_manager": "Sneha Kapoor",
        "address": "Bangalore"
    },
    {
        "client_name": "PV Sindhu",
        "risk_appetite": "Medium",
        "investment_preferences": ["Private Equity", "Equity"],
        "relationship_manager": "Ankit Verma",
        "address": "Hyderabad"
    },
    {
        "client_name": "Sachin Tendulkar",
        "risk_appetite": "Low",
        "investment_preferences": ["Government Bonds", "FD"],
        "relationship_manager": "Ravi Mehra",
        "address": "Mumbai"
    },
    {
        "client_name": "Ranveer Singh",
        "risk_appetite": "Medium",
        "investment_preferences": ["REITs", "Mutual Funds"],
        "relationship_manager": "Sneha Kapoor",
        "address": "Mumbai"
    },
    {
        "client_name": "Hrithik Roshan",
        "risk_appetite": "Medium",
        "investment_preferences": ["Balanced Funds", "Real Estate"],
        "relationship_manager": "Sneha Kapoor",
        "address": "Mumbai"
    },
    {
        "client_name": "KL Rahul",
        "risk_appetite": "High",
        "investment_preferences": ["Equity", "Crypto"],
        "relationship_manager": "Neha Shah",
        "address": "Bangalore"
    },
    {
        "client_name": "Rishabh Pant",
        "risk_appetite": "Medium",
        "investment_preferences": ["Startups", "Index Funds"],
        "relationship_manager": "Rajesh Mehta",
        "address": "Delhi"
    }
]

# Insert into MongoDB
collection.insert_many(clients)
print(" Realistic client profiles inserted successfully.")
