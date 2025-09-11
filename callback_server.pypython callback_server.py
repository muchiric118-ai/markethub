from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/result", methods=["POST"])
def result():
    data = request.json
    print("📩 Result received:", data)
    return jsonify({"ResultCode": 0, "ResultDesc": "Result received successfully"}@app.route("/timeout", methods=["POST"])
def timeout():
    data = request.json
    print("⏱ Timeout received:", data)
    return jsonify({"ResultCode": 1, "ResultDesc": "Timeout received"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)O

