def get_intent(text: str) -> str:
    t = (text or "").lower().strip()

    if any(w in t for w in ["hi", "hello", "hey", "hii"]):
        return "greeting"
    if any(w in t for w in ["bye", "goodbye", "exit", "quit"]):
        return "bye"
    if "your name" in t or "who are you" in t:
        return "bot_name"
    if "help" in t or "what can you do" in t:
        return "help"

    return "unknown"
