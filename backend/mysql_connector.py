# mysql_connector.py

import mysql.connector
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

def get_transactions_from_mysql():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "localhost"),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", "Login@630"),
            database=os.getenv("MYSQL_DB", "wealth_portfolio"),
        )
        query = "SELECT * FROM transactions"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        print("Error fetching transactions:", e)
        return pd.DataFrame()
