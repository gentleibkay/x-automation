BADWORDS = {
    "fuck", "shit", "bitch", "nigga", "nigger",
    "rape", "kill", "terrorist", "isis"
}

def passes_checks(text: str) -> bool:
    """Simple text moderation filter."""
    if not text:
        return False

    t = text.lower()

    # block profanity
    for bad in BADWORDS:
        if bad in t:
            return False

    # block extremely long texts
    if len(text) > 300:
        return False

    return True

