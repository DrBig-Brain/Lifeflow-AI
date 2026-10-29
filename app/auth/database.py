from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
import certifi

load_dotenv()

client = AsyncIOMotorClient(
  os.getenv("MONGODB_CONNECT_URI"),
  tlsCAFile=certifi.where()
)
db = client[os.getenv("DB_NAME")]

users_collection = db["users"]
