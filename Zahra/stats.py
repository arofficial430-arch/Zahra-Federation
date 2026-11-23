
from .database import get_collection


async def get_federation_stats():
    federations = await get_collection("federations")
    warnings = await get_collection("warnings")

    total_federations = await federations.count_documents({})

    total_warnings = await warnings.count_documents({})

    total_groups = 0
    total_banned = 0

    async for federation in federations.find({}):
        total_groups += len(federation.get("chats", []))
        total_banned += len(
            federation.get("banned_users", [])
        )

    return {
        "federations": total_federations,
        "groups": total_groups,
        "banned_users": total_banned,
        "warnings": total_warnings
    }


async def format_stats():
    stats = await get_federation_stats()

    return (
        "💜 ZAHRA FEDERATION STATS\n\n"
        f"🌐 Federations: {stats['federations']}\n"
        f"👥 Connected Groups: {stats['groups']}\n"
        f"🚫 Global Bans: {stats['banned_users']}\n"
        f"⚠️ Total Warnings: {stats['warnings']}"
    )
