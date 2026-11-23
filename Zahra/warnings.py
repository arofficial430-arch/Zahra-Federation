
from .database import add_warning, get_warnings, clear_warnings

MAX_WARNINGS = 3


async def warn_user(user_id, chat_id, reason="No reason provided"):
    await add_warning(user_id, chat_id, reason)

    count = await get_warnings(user_id, chat_id)

    return {
        "count": count,
        "max_warnings": MAX_WARNINGS,
        "limit_reached": count >= MAX_WARNINGS
    }


async def get_user_warning_count(user_id, chat_id):
    return await get_warnings(user_id, chat_id)


async def reset_user_warnings(user_id, chat_id):
    await clear_warnings(user_id, chat_id)
    return True
