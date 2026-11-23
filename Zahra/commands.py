
from pyrogram import filters
from .database import get_collection
from .stats import format_stats


def register_commands(app):

    @app.on_message(filters.command("newfed") & filters.group)
    async def newfed(client, message):
        if not message.from_user:
            return

        member = await client.get_chat_member(
            message.chat.id,
            message.from_user.id
        )

        if member.status not in ("administrator", "owner"):
            return await message.reply_text(
                "Only group admins can create a federation."
            )

        fed_name = f"Zahra_{message.chat.id}"

        collection = await get_collection("federations")

        existing = await collection.find_one(
            {"name": fed_name}
        )

        if existing:
            return await message.reply_text(
                "Federation already exists!"
            )

        await collection.insert_one({
            "name": fed_name,
            "owner_id": message.from_user.id,
            "chats": [message.chat.id],
            "banned_users": []
        })

        await message.reply_text(
            f"💜 Federation created!\n\n"
            f"Name: {fed_name}"
        )

    @app.on_message(filters.command("fedstats"))
    async def fedstats(client, message):
        stats = await format_stats()
        await message.reply_text(stats)

    @app.on_message(filters.command("fedinfo"))
    async def fedinfo(client, message):
        collection = await get_collection("federations")

        fed = await collection.find_one(
            {"chats": message.chat.id}
        )

        if not fed:
            return await message.reply_text(
                "This group is not in a federation."
            )

        await message.reply_text(
            f"💜 Federation Info\n\n"
            f"Name: {fed['name']}\n"
            f"Groups: {len(fed['chats'])}\n"
            f"Global bans: {len(fed['banned_users'])}"
        )
