
from pyrogram import filters


async def is_admin(client, chat_id, user_id):
    try:
        member = await client.get_chat_member(
            chat_id, user_id
        )
        return member.status in (
            ("administrator", "owner")
        )
    except Exception:
        return False


async def check_bot_protection(client, message):
    user = message.from_user

    if not user or not user.is_bot:
        return False

    if await is_admin(client, message.chat.id, user.id):
        return False

    return True


async def check_channel_protection(message):
    if message.sender_chat:
        return True

    return False
