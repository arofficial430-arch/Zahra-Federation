import os
import logging
import asyncio
from Zahra.database import create_federation, connect_database
from Zahra.database import (
    add_fed_admin,
    remove_fed_admin,
    get_fed_admins,
    add_fed_ban,
    remove_fed_ban,
    get_fed_bans,
    connect_fed_chat,
    disconnect_fed_chat,
    get_fed_chats,
    subscribe_fed,
    unsubscribe_fed,
    get_fed_subscriptions,
    get_fed_details
)
from Zahra.database import get_federation
from aiohttp import web
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
from pyrogram import Client, filters, idle
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus
# ==============================
# ZAHRA FEDERATION CONFIG
# ==============================

API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
OWNER_ID = int(os.environ.get("OWNER_ID", "0"))

# ==============================
# LOGGING
# ==============================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("ZahraFederation")

# ==============================
# BOT CLIENT
# ==============================

app = Client(
    "ZahraFederation",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ==============================
# START COMMAND
# ==============================

@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message: Message):
    logger.info("START command received")
    try:
        await message.reply_text(
            "✨ Welcome to ZAHRA FEDERATION ✨\n\n"
            "Advanced Telegram Group Management Bot\n\n"
            "Use /help to see my commands."
        )
        logger.info("START reply sent successfully")
    except Exception:
        logger.exception("START reply failed")

# ==============================
# HELP COMMAND
# ==============================

@app.on_message(filters.command("help"))
async def help_command(client, message: Message):
    await message.reply_text(
        "🔥 ZAHRA FEDERATION COMMANDS 🔥\n\n"
        "/start - Start bot\n"
        "/help - Help menu\n"
        "/id - Get chat ID\n"
        "/ping - Check bot status\n"
        "/info - Bot information"
    )

@app.on_message(filters.command("newfed") & filters.group)
async def newfed_command(client, message: Message):
    if not message.from_user:
        return

    member = await client.get_chat_member(
        message.chat.id,
        message.from_user.id
    )

    if member.status not in (
        ChatMemberStatus.OWNER,
        ChatMemberStatus.ADMINISTRATOR
    ):
        return await message.reply_text(
            "⛔ Group admins only!"
        )

    name = " ".join(message.command[1:]).strip()

    if not name:
        return await message.reply_text(
            "💜 Federation name கொடு!\n\n"
            "Example: /newfed Zahra Family"
        )

    try:
        result = await create_federation(
            name,
            message.from_user.id,
            message.chat.id
        )

        if result is None:
            return await message.reply_text(
                "⚠️ இந்த group-க்கு ஏற்கனவே Federation இருக்கு!"
            )

        await message.reply_text(
            f"🎉 Federation Created Successfully!\n\n"
            f"💜 Name: {name}\n"
            f"🆔 ID: `{result}`"
        )

    except Exception:
        logger.exception("Federation creation failed")
        await message.reply_text(
            "❌ Federation create செய்ய முடியவில்லை. Try again later!"
        )
@app.on_message(filters.command("fedinfo") & filters.group)
async def fedinfo_command(client, message: Message):
    try:
        federation = await get_federation(message.chat.id)

        if not federation:
            return await message.reply_text(
                "❌ இந்த group எந்த Federation-லயும் இல்லை!"
            )

        await message.reply_text(
            f"💜 **Federation Information**\n\n"
            f"🏷️ Name: {federation['name']}\n"
            f"🆔 ID: `{federation['_id']}`\n"
            f"👑 Owner ID: `{federation['owner_id']}`"
        )

    except Exception:
        logger.exception("Federation info failed")
        await message.reply_text(
            "❌ Federation info எடுக்க முடியவில்லை!"
        )
        
@app.on_message(filters.command("fedadmin") & filters.group)
async def fedadmin_command(client, message: Message):
    if not message.from_user:
        return

    federation = await get_federation(message.chat.id)

    if not federation:
        return await message.reply_text(
            "❌ இந்த group Federation-ல் இல்லை!"
        )

    if len(message.command) < 2 or message.command[1].lower() != "add":
        return await message.reply_text(
            "Usage: /fedadmin add (reply to user)"
        )

    if not message.reply_to_message:
        return await message.reply_text(
            "⚠️ ஒரு user message-க்கு reply செய்து /fedadmin add அனுப்பு!"
        )

    user = message.reply_to_message.from_user

    if not user:
        return await message.reply_text("❌ User கிடைக்கவில்லை!")

    if user.id == federation["owner_id"]:
        return await message.reply_text(
            "👑 Federation Owner ஏற்கனவே Owner தான்!"
        )

    try:
        await add_fed_admin(
            federation["_id"],
            user.id
        )

        await message.reply_text(
            f"🛡️ Federation Admin Added!\n\n"
            f"👤 User: {user.mention}\n"
            f"🆔 ID: `{user.id}`"
        )

    except Exception:
        logger.exception("Fed admin add failed")
        await message.reply_text(
            "❌ Admin add செய்ய முடியவில்லை!"
        )

# ==============================
# PING COMMAND
# ==============================

@app.on_message(filters.command("ping"))
async def ping_command(client, message: Message):
    await message.reply_text(
        "💜 ZAHRA FEDERATION IS ONLINE!\n"
        "Status: Active"
    )

# ==============================
# ID COMMAND
# ==============================

@app.on_message(filters.command("id"))
async def id_command(client, message: Message):
    await message.reply_text(
        f"Chat ID: `{message.chat.id}`\n"
        f"Your ID: `{message.from_user.id if message.from_user else 'Unknown'}`"
    )

# ==============================
# OWNER COMMAND
# ==============================

@app.on_message(filters.command("owner") & filters.private)
async def owner_command(client, message: Message):
    if message.from_user and message.from_user.id == OWNER_ID:
        await message.reply_text(
            "👑 Hello Owner!\n"
            "ZAHRA FEDERATION is ready."
        )
    else:
        await message.reply_text("⛔ Owner only command!")

# ==============================
# BOT INFO
# ==============================

@app.on_message(filters.command("info"))
async def info_command(client, message: Message):
    await message.reply_text(
        "💜 ZAHRA FEDERATION\n\n"
        "Version: 1.0.0\n"
        "Framework: Pyrogram\n"
        "Mode: Federation Management\n"
        "Status: Running"
    )

# ==============================
# STARTUP
# ==============================

async def health(request):
    return web.Response(text="Zahra Federation is running!")

async def main():
    logger.info("Starting Zahra Federation...")
    
    await connect_database()
    await app.start()

    web_app = web.Application()
    web_app.router.add_get("/", health)
    web_app.router.add_get("/health", health)

    runner = web.AppRunner(web_app)
    await runner.setup()

    port = int(os.environ.get("PORT", "10000"))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

    logger.info(f"HTTP server running on port {port}")

    try:
        await idle()
    finally:
        await runner.cleanup()
        await app.stop()

if __name__ == "__main__":
    loop.run_until_complete(main())
