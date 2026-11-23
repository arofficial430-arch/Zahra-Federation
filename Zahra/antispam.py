
import re
from collections import defaultdict, deque
import time

SPAM_LINKS = re.compile(
    r"(https?://|t\.me/|telegram\.me/)",
    re.IGNORECASE
)

RECENT_MESSAGES = defaultdict(lambda: deque(maxlen=10))


def check_spam(user_id, chat_id, text):
    if not text:
        return False, None

    key = (chat_id, user_id)
    normalized = text.lower().strip()

    now = time.monotonic()
    messages = RECENT_MESSAGES[key]

    # Repeated message detection
    for old_text, old_time in messages:
        if normalized == old_text and now - old_time < 15:
            return True, "Repeated message"

    messages.append((normalized, now))

    # Link detection
    if SPAM_LINKS.search(normalized):
        return True, "Link detected"

    # Excessive character detection
    if len(text) > 3000:
        return True, "Excessive message length"

    return False, None
