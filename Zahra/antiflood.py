
import time
from collections import defaultdict, deque

USER_MESSAGES = defaultdict(deque)

FLOOD_LIMIT = 7
FLOOD_TIME = 5


async def check_flood(user_id, chat_id):
    now = time.monotonic()
    key = (chat_id, user_id)

    messages = USER_MESSAGES[key]
    messages.append(now)

    while messages and now - messages[0] > FLOOD_TIME:
        messages.popleft()

    if len(messages) > FLOOD_LIMIT:
        messages.clear()
        return True

    return False


def reset_flood(user_id, chat_id):
    USER_MESSAGES.pop((chat_id, user_id), None)
