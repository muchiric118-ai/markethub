from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# === BALANCE INQUIRY CALLBACK ===
@app.route("/b2c_result", methods=["POST"])
def b2c_result():
    data = request.get_json()
    print("\n📩 B2C Result Callback Received:")
    print(json.dumps(data, indent=4))
    return jsonify({"ResultCode": 0, "ResultDesc": "Result received successfully"})

@app.route("/b2c_timeout", methods=["POST"])
def b2c_timeout():
    data = request.get_json()
    print("\n⏳ B2C Timeout Callback Received:")
    print(json.dumps(data, indent=4))
    return jsonify({"ResultCode": 0, "ResultDesc": "Timeout received successfully"})

# === BALANCE INQUIRY CALLBACK ===
@app.route("/balance_result", methods=["POST"])
def balance_result():
    data = request.get_json()
    print("\n📊 Balance Result Callback Received:")
    print(json.dumps(data, indent=4))

    # Optional: parse the balance
    try:
        account_balance = data["Result"]["ResultParameters"]["ResultParameter"][0]["Value"]
        print(f"💰 Available Balance: {account_balance}")
    except Exception as e:
        print("⚠️ Could not parse balance:", str(e))

    return jsonify({"ResultCode": 0, "ResultDesc": "Balance received successfully"})

@app.route("/balance_timeout", methods=["POST"])
def balance_timeout():
    data = request.get_json()
    print("\n⏳ Balance Timeout Callback Received:")
    print(json.dumps(data, indent=4))
    return jsonify({"ResultCode": 0, "ResultDesc": "Balance timeout received successfully"})

# === MAIN ===
if __name__ == "__main__":
    print("🚀 Callback server running on port 5000...")
    app.run(host="0.0.0.0", port=5000)
