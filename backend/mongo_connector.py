# mongo_connector.py

from pymongo import MongoClient
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = "wealth_portfolio"
COLLECTION_NAME = "client_profiles"

def get_clients_from_mongo():
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        documents = list(collection.find({}, {"_id": 0}))  # Exclude MongoDB's _id
        df = pd.DataFrame(documents)
        return df
    except Exception as e:
        print("Error fetching clients:", e)
        return pd.DataFrame()  # Return empty DataFrame on failure
