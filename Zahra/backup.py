
import json
from datetime import datetime, timezone
from pathlib import Path

from .database import get_collection

BACKUP_DIR = Path("backups")


async def create_backup():
    BACKUP_DIR.mkdir(exist_ok=True)

    collections = [
        "federations",
        "warnings",
    ]

    backup_data = {}

    for name in collections:
        collection = await get_collection(name)

        documents = await collection.find(
            {}
        ).to_list(length=None)

        for document in documents:
            document["_id"] = str(document["_id"])

        backup_data[name] = documents

    timestamp = datetime.now(
        timezone.utc
    ).strftime("%Y%m%d_%H%M%S")

    backup_file = BACKUP_DIR / f"zahra_{timestamp}.json"

    with backup_file.open("w", encoding="utf-8") as file:
        json.dump(
            backup_data,
            file,
            indent=4,
            ensure_ascii=False
        )

    return str(backup_file)


async def backup_status():
    BACKUP_DIR.mkdir(exist_ok=True)

    return list(BACKUP_DIR.glob("zahra_*.json"))
