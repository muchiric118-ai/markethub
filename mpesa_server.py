from flask import Flask, request, jsonify

app = Flask(__name__)

# Validation URL endpoint
@app.route("/validate", methods=["POST"])
def validate():
    data = request.get_json()

    print("Validation request received:", data)
    return jsonify({"ResultCode": 0, "ResultDesc": "Validation passed successfully"})

# Confirmation URL endpoint
@app.route("/confirm", methods=["POST"])
def confirm():
    data = request.get_json()
    print("Confirmation request received:", data)
    return jsonify({"ResultCode": 0, "ResultDesc": "Confirmation received successfully"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
