
from .database import get_collection


async def create_federation(owner_id, name):
    collection = await get_collection("federations")

    existing = await collection.find_one({
        "owner_id": owner_id,
        "name": name
    })

    if existing:
        return False

    result = await collection.insert_one({
        "owner_id": owner_id,
        "name": name,
        "chats": [],
        "banned_users": []
    })

    return result.inserted_id


async def get_federation(name):
    collection = await get_collection("federations")
    return await collection.find_one({"name": name})


async def join_federation(name, chat_id):
    collection = await get_collection("federations")

    return await collection.update_one(
        {"name": name},
        {"$addToSet": {"chats": chat_id}}
    )


async def leave_federation(name, chat_id):
    collection = await get_collection("federations")

    return await collection.update_one(
        {"name": name},
        {"$pull": {"chats": chat_id}}
    )


async def federation_ban(name, user_id):
    collection = await get_collection("federations")

    return await collection.update_one(
        {"name": name},
        {"$addToSet": {"banned_users": user_id}}
    )


async def federation_unban(name, user_id):
    collection = await get_collection("federations")

    return await collection.update_one(
        {"name": name},
        {"$pull": {"banned_users": user_id}}
    )
