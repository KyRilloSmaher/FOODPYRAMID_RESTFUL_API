from mongoengine import connect
from mongoengine.connection import get_db
from dotenv import load_dotenv
from pathlib import Path
import os

def init_db():

    env_path = Path(__file__).parent / ".env"
    load_dotenv(dotenv_path=env_path)
    mongo_uri = os.getenv("MONGO_URI")
    print(f"🔍 Loaded MONGO_URI: {mongo_uri}")  # Debug print

    if not mongo_uri:
        raise ValueError("❌ MONGO_URI not found in .env")

    connect(host=mongo_uri)

    db = get_db()
    print(f"✅ Connected to MongoDB database: {db.name}")
