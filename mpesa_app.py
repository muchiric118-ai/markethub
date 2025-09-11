import base64
import requests
from flask import Flask, request, jsonify

# 🔑 Replace these with your real Safaricom sandbox credentials
consumer_key = "YOUR_CONSUMER_KEY"
consumer_secret = "YOUR_CONSUMER_SECRET"
short_code = "600000"         # test shortcode (e.g. paybill or till)
test_msisdn = "254708374149"  # Safaricom sandbox test number

# ------------------------------
# 1. Generate Access Token
# ------------------------------
def get_access_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    credentials = f"{consumer_key}:{consumer_secret}"
    encoded = base64.b64encode(credentials.encode()).decode("utf-8")
    headers = {"Authorization": f"Basic {encoded}"}

    response = requests.get(url, headers=headers)
    data = response.json()
    return data["access_token"]

# ------------------------------
# 2. Register Validation & Confirmation URLs
# ------------------------------
def register_urls(base_url):
    access_token = get_access_token()
    url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": f"Bearer {access_token}"}

    payload = {
        "ShortCode": short_code,
        "ResponseType": "Completed",
        "ConfirmationURL": f"{base_url}/confirmation",
        "ValidationURL": f"{base_url}/validation"
    }

    response = requests.post(url, headers=headers, json=payload)

    print("📡 Status Code:", response.status_code)
    print("📡 Raw Response:", response.text)

    try:
        data = response.json()
        print("✅ JSON Response:", data)
        return data
    except Exception as e:
        print("⚠️ Could not decode JSON:", str(e))
        return None

# ------------------------------
# 3. Simulate a C2B Payment
# ------------------------------
def simulate_c2b():
    access_token = get_access_token()
    url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate"
    headers = {"Authorization": f"Bearer {access_token}"}

    payload = {
        "ShortCode": short_code,
        "CommandID": "CustomerPayBillOnline",
        "Amount": "100",
        "Msisdn": test_msisdn,
        "BillRefNumber": "Test123"
    }

    response = requests.post(url, headers=headers, json=payload)

    print("📡 Status Code:", response.status_code)
    print("📡 Raw Response:", response.text)

    try:
        data = response.json()
        print("💰 Simulate C2B response:", data)
        return data
    except Exception as e:
        print("⚠️ Could not decode JSON:", str(e))
        return None

# ------------------------------
# 4. Flask Server
# ------------------------------
app = Flask(__name__)

@app.route("/confirmation", methods=["POST"])
def confirmation():
    data = request.json
    print("✅ Confirmation received:", data)
    return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"})

@app.route("/validation", methods=["POST"])
def validation():
    data = request.json
    print("✅ Validation received:", data)
    return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"})

if __name__ == "__main__":
    print("🚀 Flask server starting on port 5000...")
    app.run(host="0.0.0.0", port=5000)
