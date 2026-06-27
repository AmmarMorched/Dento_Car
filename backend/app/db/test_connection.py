# test_supabase_connection.py
import os
from supabase import create_client, Client
from dotenv import load_dotenv
from pathlib import Path

# Load .env
backend_dir = Path(__file__).parent.parent.parent
env_path = backend_dir / '.env'
load_dotenv(dotenv_path=env_path)

supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")

print(f"📡 Testing connection to: {supabase_url}")
print(f"🔑 Key present: {'Yes' if supabase_key else 'No'}")

try:
    # Create the client
    supabase: Client = create_client(supabase_url, supabase_key)
    
    # Simple test - try to get the current session
    # This doesn't require any tables
    response = supabase.auth.get_session()
    
    print("✅ Connection successful!")
    print(f"📊 Response: {response}")
    
except Exception as e:
    print(f"❌ Connection failed: {e}")