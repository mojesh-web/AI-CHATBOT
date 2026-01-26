from nlp import get_intent
from responses import get_response

print("🤖 Chatbot started! Type 'bye' to exit.")

while True:
    user_input = input("You: ")

    intent = get_intent(user_input)
    response = get_response(intent)

    print("Bot:", response)

    if intent == "bye":
        break
