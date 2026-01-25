print("Hello! I am your first chatbot 🤖")

while True:
    user = input("You: ")
    if user.lower() == "bye":
        print("Bot: Goodbye 👋")
        break
    else:
        print("Bot: You said:", user)
