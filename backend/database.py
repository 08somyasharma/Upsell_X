import os
from dotenv import load_dotenv
from pymongo import MongoClient
import certifi

load_dotenv()

MONGO_URL = os.getenv("MONGODB_URI", "").strip().strip('"').strip("'")

client = MongoClient(
    MONGO_URL,
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=5000
)

db = client["upsellx"]
admins_collection = db["admins"]