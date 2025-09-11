from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/callback", methods=["POST"])
def mpesa_callback():
    data = request.get_json()
    print("📥 Callback Data:", data)  # Print to terminal
    # You can also save this to a database/file for records

    # Send response back to Safaricom
    return jsonify({"ResultCode": 0, "ResultDesc": "Callback received successfully"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
