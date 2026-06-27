# test_pooler.py
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv('/home/morched/Desktop/DentoCar/backend/.env')

DATABASE_URL = os.getenv('DATABASE_URL')

print(f"Testing connection to: {DATABASE_URL}")

try:
    # Try connecting with the new URL
    conn = psycopg2.connect(DATABASE_URL, connect_timeout=10)
    
    cur = conn.cursor()
    cur.execute('SELECT version();')
    version = cur.fetchone()[0]
    
    print("✅ Connection successful!")
    print(f"PostgreSQL version: {version}")
    
    # List tables
    cur.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public';")
    tables = cur.fetchall()
    print(f"Tables in public schema: {tables}")
    
    cur.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Connection failed: {e}")
    print("\nTroubleshooting tips:")
    print("1. Check if the pooler hostname is correct")
    print("2. Verify your password is correct")
    print("3. Make sure the database name is correct")