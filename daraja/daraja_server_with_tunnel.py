import subprocess
import threading
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- Flask Routes ---
@app.route("/")
def home():
    return "Daraja Flask server is running."

@app.route("/stk_callback", methods=["POST"])
def stk_callback():
    data = request.get_json()
    print("📩 Callback received:", data)
    return jsonify({"ResultCode": 0, "ResultDesc": "Callback received successfully"})


def run_flask():
    app.run(host="0.0.0.0", port=5000, debug=True)


def run_cloudflared():
    # Start cloudflared tunnel
    process = subprocess.Popen(
        ["cloudflared", "tunnel", "--url", "http://localhost:5000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    # Parse logs and print the public URL
    for line in process.stdout:
        print(line, end="")
        if "trycloudflare.com" in line:
            print("🌍 Public URL:", line.strip())


if __name__ == "__main__":
    # Run Flask in a thread
    threading.Thread(target=run_flask, daemon=True).start()

    # Give Flask a moment to boot
    time.sleep(3)

    # Run cloudflared in main thread
    run_cloudflared()
