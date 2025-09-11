import base64
import requests
import json
import time
from flask import Flask, request

# -------------------
# Hardcoded Credentials
# -------------------
CONSUMER_KEY = "IJbHP70UyXidTKyYdIqUC8E52CrFIcrr1DDGvmL9BKGhfKt2"
CONSUMER_SECRET = "ZcUwSvLaLKH51GO3Jqa4bwY5URfZBkd3Tioo2e4erBG9vslOGRQUf1QrmfAuDCqU"
SECURITY_CREDENTIAL = "js4SqxpKWpKFbEhRMK0G7p2MdCrgaxUfG+n/v56ONlLkNZUD7bXLHG8W426P5ir1illnqIAtxisE6iJQ6cysE2zP4OddLdqaSnL//AlfaQgRMu2G7EHsIimVOxLGVUj3BU6y81+pkAyMTmDycdnODUQk8/0Cxw+nPl98GavDz10Wv7vQizjjcc1ZueWvuXWSWxbClG2cMq7/attqIhI6Fvfxm9BVGKDKkNxp/EqjXxdNwwk8Mp4yHE8AEu4QF5P9LH/tJ9B2muvmcGlOBSPAo6YbRgujjQggPimj79j9pvnYsV77MUSs/pSjuGY0q04CMtJ2M7bv1xEJb9UtNxWxcA=="
INITIATOR_NAME = "Dasch"
SHORTCODE = "8286400"
FIXED_RECIPIENT = "254729149198"

# -------------------
# Flask App
# -------------------
app = Flask(__name__)

access_token = None
base_url = "https://api.safaricom.co.ke"   # Production

# -------------------
# Get OAuth Token
# -------------------
def get_access_token():
    global access_token
    url = f"{base_url}/oauth/v1/generate?grant_type=client_credentials"
    resp = requests.get(url, auth=(CONSUMER_KEY, CONSUMER_SECRET))
    access_token = resp.json().get("access_token")
    print(f"✅ Got access token: {access_token[:10]}...")

# -------------------
# Balance Callback
# -------------------
@app.route("/balance_callback", methods=["POST"])
def balance_callback():
    data = request.json
    print("📩 Balance Callback:", json.dumps(data, indent=2))

    try:
        result = data["Result"]
        balance_str = result["ResultParameters"]["ResultParameter"][0]["Value"]
        balance = float(balance_str.split()[0].replace(",", ""))  # e.g. "12345.00 KES"

        print(f"💰 Balance available: {balance} KES")
        if balance > 0:
            amount_to_send = int(balance - 30)  # leave safe margin of 30
            if amount_to_send > 0:
                print(f"➡️ Sending {amount_to_send} to {FIXED_RECIPIENT}")
                b2c_request(amount_to_send)
    except Exception as e:
        print(f"❌ Error parsing balance: {e}")
    return "OK"

# -------------------
# B2C Payout
# -------------------
def b2c_request(amount):
    url = f"{base_url}/mpesa/b2c/v1/paymentrequest"
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {
        "InitiatorName": INITIATOR_NAME,
        "SecurityCredential": SECURITY_CREDENTIAL,
        "CommandID": "BusinessPayment",
        "Amount": amount,
        "PartyA": SHORTCODE,
        "PartyB": FIXED_RECIPIENT,
        "Remarks": "Auto payout",
        "QueueTimeOutURL": "https://screw-meetup-pins-arbitration.trycloudflare.com/timeout",
        "ResultURL": "https://screw-meetup-pins-arbitration.trycloudflare.com/result",
        "Occasion": "BalanceAuto"
    }
    resp = requests.post(url, headers=headers, json=payload)
    print("📤 B2C Response:", resp.text)

# -------------------
# Trigger Balance Check
# -------------------
def check_balance():
    url = f"{base_url}/mpesa/accountbalance/v1/query"
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {
        "Initiator": INITIATOR_NAME,
        "SecurityCredential": SECURITY_CREDENTIAL,
        "CommandID": "AccountBalance",
        "PartyA": SHORTCODE,
        "IdentifierType": "4",
        "Remarks": "BalanceCheck",
        "QueueTimeOutURL": "https://screw-meetup-pins-arbitration.trycloudflare.com/timeout",
        "ResultURL": "https://screw-meetup-pins-arbitration.trycloudflare.com/balance_callback"
    }
    resp = requests.post(url, headers=headers, json=payload)
    print("📤 Balance Request sent:", resp.text)

# -------------------
# Main
# -------------------
if __name__ == "__main__":
    get_access_token()
    # Start Flask in background
    from threading import Thread
    Thread(target=lambda: app.run(host="0.0.0.0", port=5000)).start()

    time.sleep(3)  # wait for Flask to be ready
    check_balance()
