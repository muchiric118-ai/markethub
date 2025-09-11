from flask import Flask, request, jsonify
import logging, requests, base64, datetime as dt, os

BOT_TOKEN = "8438109353:AAEUGWgORF7lT7esLb-fylr4Ov8deSfq7I8"
ADMIN_ID = 1923615279
PHONE_NUMBER = "0729149198"

CONSUMER_KEY = "IJbHP70UyXidTKyYdIqUC8E52CrFIcrr1DDGvmL9BKGhfKt2"
CONSUMER_SECRET = "ZcUwSvLaLKH51GO3Jqa4bwY5URfZBkd3Tioo2e4erBG9vslOGRQUf1QrmfAuDCqU"
SHORTCODE = "5185413"
PASSKEY = "KlH4l/Pm81YYDqi8+KU/dRZYWKJMBtR9gi2FVG0qL+E3ZYs24vHjlHXuWmQ6PqbKuut2CDeRG4WmV/fK4nn6vyfUuzMylunBn3j50cMdLJxyS1b6xQGYyihkbuHnrtn2zyf6vDvADIq2ruwqVmAZD3wNGfrhGcQMU3l6Mj3bv3dMlzglaTDv7xN/Q7FbRjBNrOajH+JoAGYy9z2D9g1jXmvvyXs0QLvd2arPEp3BOxIYiFDOf1b6r6VyZT8VdURixLeXhQTjkUpMEE1J4WyitbTO1Dvu6ZLB7rY/A+IX1ccE8A9Rt7GtjzuFHPj/ZdOHzHBN2L4IEDb8N6nzwZhiyg=="

TOKEN_URL = "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
STK_URL = "https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

def get_access_token():
    r = requests.get(TOKEN_URL, auth=(CONSUMER_KEY, CONSUMER_SECRET))
    return r.json()["access_token"]

def stk_push(amount, phone):
    token = get_access_token()
    timestamp = dt.datetime.now().strftime("%Y%m%d%H%M%S")
    password = base64.b64encode((SHORTCODE + PASSKEY + timestamp).encode()).decode()

    payload = {
        "BusinessShortCode": SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone,
        "PartyB": SHORTCODE,
        "PhoneNumber": phone,
        "CallBackURL": f"{os.getenv('PUBLIC_URL')}/mpesa_callback",
        "AccountReference": "TelegramBot",
        "TransactionDesc": "Payment via Bot"
    }

    r = requests.post(STK_URL, json=payload, headers={"Authorization": f"Bearer {token}"})
    return r.json()

@app.route("/webhook/" + BOT_TOKEN, methods=["POST"])
def telegram_webhook():
    update = request.get_json()
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")

        if text.startswith("/pay"):
            try:
                _, amt, phone = text.split()
                res = stk_push(int(amt), phone)
                send_message(chat_id, f"STK Push sent: {res}")
            except Exception as e:
                send_message(chat_id, f"Error: {e}")
    return jsonify(ok=True)

@app.route("/health", methods=["GET"])
def health():
    return "OK", 200

def send_message(chat_id, text):
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                  json={"chat_id": chat_id, "text": text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
