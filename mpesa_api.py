# mpesa_api.py

import requests
import base64
import datetime

# 🔑 Replace with your Daraja sandbox credentials
consumer_key = "IJbHP70UyXidTKyYdIqUC8E52CrFIcrr1DDGvmL9BKGhfKt2"
consumer_secret = "ZcUwSvLaLKH51GO3Jqa4bwY5URfZBkd3Tioo2e4erBG9vslOGRQUf1QrmfAuDCqU"
shortcode = "174379"   # test shortcode from Safaricom sandbox
passkey = "YOUR_PASSKEY"  # from Daraja portal
phone_number = "254729149198"

# ===============================
# Get OAuth Token
# ===============================
def get_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(url, auth=(consumer_key, consumer_secret))
    response.raise_for_status()
    return response.json()["access_token"]

# ===============================
# STK Push (Lipa na Mpesa Online)
# ===============================
def stk_push(amount=1, account_reference="Test", transaction_desc="Payment"):
    token = get_token()
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

    # Timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    # Password = base64(shortcode + passkey + timestamp)
    password = base64.b64encode((shortcode + passkey + timestamp).encode()).decode("utf-8")

    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "BusinessShortCode": shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": shortcode,
        "PhoneNumber": phone_number,
        "CallBackURL": "https://mydomain.com/path",  # replace with your callback URL
        "AccountReference": account_reference,
        "TransactionDesc": transaction_desc,
    }

    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

# ===============================
# Debug quick run
# ===============================
if __name__ == "__main__":
    print("🔑 Access Token:", get_token())
    print("📲 Sending STK push...")
    print(stk_push(amount=10))
