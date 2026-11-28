
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
    
# ==============================
# ZAHRA FEDERATION DATABASE
# ==============================

async def add_fed_admin(fed_id, user_id):
    collection = await get_collection("fed_admins")
    return await collection.update_one(
        {"fed_id": str(fed_id), "user_id": user_id},
        {"$set": {"fed_id": str(fed_id), "user_id": user_id}},
        upsert=True
    )


async def remove_fed_admin(fed_id, user_id):
    collection = await get_collection("fed_admins")
    return await collection.delete_one({
        "fed_id": str(fed_id),
        "user_id": user_id
    })


async def get_fed_admins(fed_id):
    collection = await get_collection("fed_admins")
    return await collection.count_documents({
        "fed_id": str(fed_id)
    })


async def add_fed_ban(fed_id, user_id, reason="No reason"):
    collection = await get_collection("fed_bans")
    return await collection.update_one(
        {"fed_id": str(fed_id), "user_id": user_id},
        {"$set": {
            "fed_id": str(fed_id),
            "user_id": user_id,
            "reason": reason
        }},
        upsert=True
    )


async def remove_fed_ban(fed_id, user_id):
    collection = await get_collection("fed_bans")
    return await collection.delete_one({
        "fed_id": str(fed_id),
        "user_id": user_id
    })


async def get_fed_bans(fed_id):
    collection = await get_collection("fed_bans")
    return await collection.count_documents({
        "fed_id": str(fed_id)
    })


async def connect_fed_chat(fed_id, chat_id):
    collection = await get_collection("fed_chats")
    return await collection.update_one(
        {"fed_id": str(fed_id), "chat_id": chat_id},
        {"$set": {
            "fed_id": str(fed_id),
            "chat_id": chat_id
        }},
        upsert=True
    )


async def disconnect_fed_chat(fed_id, chat_id):
    collection = await get_collection("fed_chats")
    return await collection.delete_one({
        "fed_id": str(fed_id),
        "chat_id": chat_id
    })


async def get_fed_chats(fed_id):
    collection = await get_collection("fed_chats")
    return await collection.count_documents({
        "fed_id": str(fed_id)
    })


async def subscribe_fed(fed_id, subscribed_fed_id):
    collection = await get_collection("fed_subscriptions")
    return await collection.update_one(
        {
            "fed_id": str(fed_id),
            "subscribed_fed_id": str(subscribed_fed_id)
        },
        {"$set": {
            "fed_id": str(fed_id),
            "subscribed_fed_id": str(subscribed_fed_id)
        }},
        upsert=True
    )


async def unsubscribe_fed(fed_id, subscribed_fed_id):
    collection = await get_collection("fed_subscriptions")
    return await collection.delete_one({
        "fed_id": str(fed_id),
        "subscribed_fed_id": str(subscribed_fed_id)
    })


async def get_fed_subscriptions(fed_id):
    collection = await get_collection("fed_subscriptions")
    return await collection.count_documents({
        "fed_id": str(fed_id)
    })


async def get_fed_details(fed_id):
    collection = await get_collection("federations")
    return await collection.find_one({
        "_id": fed_id
    })
