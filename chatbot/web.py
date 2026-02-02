from flask import Flask, render_template, request
from chatbot.nlp import get_intent
from chatbot.responses import get_response
from chatbot.faq import find_faq_answer

app = Flask(__name__)

# Store chat messages (resets when server restarts)
chat_history = []

@app.route("/", methods=["GET", "POST"])
def home():
    global chat_history

    if request.method == "POST":
        user_text = request.form.get("message", "").strip()

        if user_text:
            # store user message
            chat_history.append(("You", user_text))

            # 1) try FAQ knowledge base
            faq_answer = find_faq_answer(user_text)

            if faq_answer:
                bot_text = faq_answer
            else:
                # 2) fallback to intent-based replies
                intent = get_intent(user_text)
                bot_text = get_response(intent)

            # store bot message
            chat_history.append(("Bot", bot_text))

    return render_template("chat.html", chat_history=chat_history)


if __name__ == "__main__":
    app.run(debug=True)
