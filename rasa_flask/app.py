from flask import Flask, render_template, request, jsonify
import requests

RASA_API_URL = "http://localhost:5005/webhooks/rest/webhook"
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        user_message = request.json["message"]
        print("User Message:", user_message)

        # Send user message to Rasa and get bot's response
        rasa_response = requests.post(RASA_API_URL, json={"message": user_message})

        # Raise an HTTPError for bad responses
        rasa_response.raise_for_status()

        rasa_response_json = rasa_response.json()

        print("Rasa Response:", rasa_response_json)

        if rasa_response_json and isinstance(rasa_response_json, list) and "text" in rasa_response_json[0]:
            bot_response = rasa_response_json[0]["text"]
        else:
            bot_response = "Sorry, I didn't understand that."

        return jsonify({"response": bot_response})

    except Exception as e:
        # Handle exceptions (e.g., network issues, invalid JSON, etc.)
        print("Error:", str(e))
        return jsonify({"response": "An error occurred. Please try again."})

if __name__ == "__main__":
    app.run(debug=True, port=3000)
