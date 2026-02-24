import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")

if not MONGO_URL:
    raise ValueError("MONGO_URL not found in .env file")

client = MongoClient(MONGO_URL)

# Create / connect to database
db = client["SmartPowerDB_V2"]
