from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
import certifi

load_dotenv()

mongo_tls_options = (
  {"tlsCAFile": certifi.where()}
  if os.getenv("MONGODB_TLS", "true").lower() in {"1", "true", "yes"}
  else {}
)
client = AsyncIOMotorClient(os.getenv("MONGODB_CONNECT_URI"), **mongo_tls_options)
db = client[os.getenv("DB_NAME")]

users_collection = db["users"]
