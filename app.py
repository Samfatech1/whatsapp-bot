from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = "edpassare_verify_token"

@app.route("/webhook", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    else:
        return "Verification failed", 403


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("Received message:", data)
    return "OK", 200


@app.route("/")
def home():
    return "WhatsApp Bot Running"