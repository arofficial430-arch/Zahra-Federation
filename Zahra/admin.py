
import os

OWNER_ID = int(os.getenv("OWNER_ID", "0"))

SUDO_USERS = set()


def is_owner(user_id):
    return user_id == OWNER_ID


def is_sudo(user_id):
    return user_id in SUDO_USERS or is_owner(user_id)


async def is_group_admin(client, chat_id, user_id):
    try:
        member = await client.get_chat_member(
            chat_id, user_id
        )

        return member.status in (
            "administrator",
            "owner"
        )

    except Exception:
        return False


def add_sudo(user_id):
    SUDO_USERS.add(user_id)


def remove_sudo(user_id):
    SUDO_USERS.discard(user_id)


def get_sudo_users():
    return list(SUDO_USERS)
