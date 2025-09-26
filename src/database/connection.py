# src/database/connection.py
import psycopg2
import os
from dotenv import load_dotenv  # Optional: for environment variables

# Load environment variables from .env file (if you use one)
load_dotenv()

def get_db_connection():
    """
    Creates and returns a connection to the PostgreSQL database.
    Uses environment variables for security.
    """
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            database=os.getenv('DB_NAME', 'lol_database'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', ''),
            port=os.getenv('DB_PORT', '5432')
        )
        return conn
    except Exception as e:
        print(f" Error connecting to database: {e}")
        raise

