def get_response(intent: str) -> str:
    responses = {
        "greeting": "Hello! 👋 Ask me something.",
        "bot_name": "I’m your chatbot 🤖 (made by Vivek).",
        "help": "Try: 'hi', 'your name', 'bye'. We can add more skills next.",
        "bye": "Goodbye! 👋",
        "unknown": "I’m not sure yet. Try 'help' 🙂",
    }
    return responses.get(intent, "I’m not sure yet. Try 'help' 🙂")
