
import os
from motor.motor_asyncio import AsyncIOMotorClient

DATABASE_URL = os.environ.get("DATABASE_URL", "")

mongo_client = None
db = None

async def connect_database():
    global mongo_client, db

    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is missing!")

    mongo_client = AsyncIOMotorClient(DATABASE_URL)
    db = mongo_client["ZahraFederation"]

    await mongo_client.admin.command("ping")
    print("Zahra Federation Database Connected!")

async def close_database():
    global mongo_client

    if mongo_client:
        mongo_client.close()
        mongo_client = None

async def get_collection(name):
    if db is None:
        raise RuntimeError("Database is not connected!")

    return db[name]

async def add_warning(user_id, chat_id, reason):
    collection = await get_collection("warnings")

    return await collection.insert_one({
        "user_id": user_id,
        "chat_id": chat_id,
        "reason": reason
    })

async def get_warnings(user_id, chat_id):
    collection = await get_collection("warnings")

    return await collection.count_documents({
        "user_id": user_id,
        "chat_id": chat_id
    })

async def clear_warnings(user_id, chat_id):
    collection = await get_collection("warnings")

    return await collection.delete_many({
        "user_id": user_id,
        "chat_id": chat_id
    })
async def create_federation(name, owner_id, chat_id):
    collection = await get_collection("federations")

    existing = await collection.find_one({"chat_id": chat_id})

    if existing:
        return None

    result = await collection.insert_one({
        "name": name,
        "owner_id": owner_id,
        "chat_id": chat_id,
        "created": True
    })

    return result.inserted_id


async def get_federation(chat_id):
    collection = await get_collection("federations")

    return await collection.find_one({"chat_id": chat_id})
