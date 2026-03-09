from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = "samfatech_verify_token"
WHATSAPP_TOKEN = "EAA7kdrvwDzkBQ0ZB9kwm85B59CPo1uyuUjUpYHj5VS7QhSqU9yXi3ZBFZAow5QvkUeJ8PFZB4767ToSAmHFWdoOvIgodxyhEvbZBS7u9wBdL1IVKo90eVjkkk1Qm51dmWWEiTfZC0n29g8pVNOF1YvVI9JgSZAyIeUa9qIe6VGByBCdcQxYLQLRRMFSkM70LsAOydEzTG15x3WiZBuU4pJ95QRJKldsqYPIauBtoZC8HN7RSjCfqif7DFwvR2DF2xsn1X4YZAgV2EtpYW6M9nRrHrd"
PHONE_NUMBER_ID = "1041297289063742"


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
    data = request.json
    print("Incoming message:", data)

    try:
        message = data["entry"][0]["changes"][0]["value"]["messages"][0]
        phone_number = message["from"]
        text = message["text"]["body"]

        send_whatsapp_message(phone_number, f"You said: {text}")

    except:
        pass

    return "EVENT_RECEIVED", 200


def send_whatsapp_message(phone_number, message):

    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "text",
        "text": {
            "body": message
        }
    }

    requests.post(url, headers=headers, json=payload)


if __name__ == "__main__":
    app.run()