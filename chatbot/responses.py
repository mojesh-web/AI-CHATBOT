def get_response(intent):
    responses = {
        "greeting": "Hello! 👋 How can I help you?",
        "how_are_you": "I'm doing great! Thanks for asking 😊",
        "bye": "Goodbye! Have a nice day 🌟",
        "unknown": "Sorry, I didn't understand that 🤔"
    }

    return responses.get(intent)
