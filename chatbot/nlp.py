def get_intent(user_input):
    user_input = user_input.lower()

    if any(word in user_input for word in ["hi", "hello", "hey"]):
        return "greeting"

    elif any(word in user_input for word in ["bye", "goodbye", "exit"]):
        return "bye"

    elif any(word in user_input for word in ["how", "are", "you"]):
        return "how_are_you"

    else:
        return "unknown"
