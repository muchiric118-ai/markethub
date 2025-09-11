from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/stk_callback", methods=["POST"])
def stk_callback():
    data = request.get_json()
    print("📩 STK Push Callback Received:", data)

    if data and "Body" in data and "stkCallback" in data["Body"]:
        callback = data["Body"]["stkCallback"]
        if "CallbackMetadata" in callback:
            items = callback["CallbackMetadata"]["Item"]
            receipt = next((item["Value"] for item in items if item["Name"] == "MpesaReceiptNumber"), None)
            amount = next((item["Value"] for item in items if item["Name"] == "Amount"), None)
            phone = next((item["Value"] for item in items if item["Name"] == "PhoneNumber"), None)

            print(f"✅ Payment Success: Receipt={receipt}, Amount={amount}, Phone={phone}")

            return jsonify({"ResultCode": 0, "ResultDesc": "Received successfully"})
    
    return jsonify({"ResultCode": 1, "ResultDesc": "No valid data"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
stk_push_payload = {
    "BusinessShortCode": "174379",
    "Password": password,
    "Timestamp": timestamp,
    "TransactionType": "CustomerPayBillOnline",
    "Amount": "1",
    "PartyA": "2547XXXXXXXX",
    "PartyB": "174379",
    "PhoneNumber": "2547XXXXXXXX",
    "CallBackURL": "https://capacity-burn-alternatives-edinburgh.trycloudflare.com/stk_callback",
    "AccountReference": "Test123",
    "TransactionDesc": "Payment"
}
