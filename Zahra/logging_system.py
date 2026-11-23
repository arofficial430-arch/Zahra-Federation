
import logging
from datetime import datetime, timezone

logger = logging.getLogger("ZahraFederation")


async def log_action(
    action,
    admin_id=None,
    user_id=None,
    chat_id=None,
    reason="No reason provided"
):
    timestamp = datetime.now(
        timezone.utc
    ).strftime("%Y-%m-%d %H:%M:%S UTC")

    logger.info(
        "ACTION=%s | ADMIN=%s | USER=%s | CHAT=%s | REASON=%s | TIME=%s",
        action,
        admin_id,
        user_id,
        chat_id,
        reason,
        timestamp
    )


async def log_error(error):
    logger.exception(
        "Zahra Federation Error: %s",
        error
    )
