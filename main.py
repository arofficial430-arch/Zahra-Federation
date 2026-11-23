import os
import logging
import asyncio
from aiohttp import web
from pyrogram import Client, filters, idle
from pyrogram.types import Message

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
    asyncio.run(main())
