from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from datetime import datetime
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

decision_collection = db['decision']

async def save_decision(
        decision_id : str,
        user_id : str,
        question : str,
        recommendation : str,
        reasoning : str,
)-> None:
    await decision_collection.insert_one({
        "decision_id": decision_id,
        "user_id":user_id,
        "question":question,
        "recommendation":recommendation,
        "reasoning":reasoning,
        "timestamp": datetime.now().isoformat(),
    })
async def get_past_decision(user_id:str | None, limit: int = 5) -> list[dict]: 
    uid = user_id or "anonymous"
    cursor = decision_collection.find(
        {"user_id":uid},
        {"_id":0}
    ).sort("timestamp",-1).limit(limit)
    return await cursor.to_list(length=limit)
