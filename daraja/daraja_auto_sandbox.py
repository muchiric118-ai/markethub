#!/usr/bin/env python3
"""
daraja_auto_sandbox.py

Single-file sandbox-safe Daraja flow:

- Start Flask server on port 5000 to receive callbacks
- Start cloudflared quick tunnel and capture public URL
- Request AccountBalance (sandbox) with ResultURL -> callback
- Wait for balance callback, parse available balance
- Immediately call sandbox B2C API with parsed balance
- Print minimal console output (balance + B2C response)
- Keep server running briefly to accept callbacks, then exit

EDIT the placeholders below with your SANDBOX credentials before running.
Do NOT use production credentials in this file.
"""

import subprocess
import threading
import time
import re
import sys
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# ---------------------------
# === SANDBOX CREDENTIALS ===
# Replace these with your SANDBOX credentials from Safaricom dev portal
# ---------------------------
CONSUMER_KEY = "IJbHP70UyXidTKyYdIqUC8E52CrFIcrr1DDGvmL9BKGhfKt2"
CONSUMER_SECRET = "ZcUwSvLaLKH51GO3Jqa4bwY5URfZBkd3Tioo2e4erBG9vslOGRQUf1QrmfAuDCqU"
SECURITY_CREDENTIAL = "gekGxt01lhIlxSDyeaSCeEvn+4aZnsceursg5O2MM+7aH6ClDIB+zy33me7dxX4TbUsFIOyGRknrZJYFe2cdSCQJ4dSkwdDsGe/de4m96QhSi40HM+w+XpmlT+lnV7z9uCLWkjBg7ST69qpICmuO4fkCpK6vDZwEDPCmBdJT2krJSzLq5BJ+XjY1c6w4ChpUjbdBTuP36433N4oEMNZnxqN2PGqCZiabeXx4L7wrO/M1Sygy4paMezz4LKzvdx0SZudRxLNWPgHHBQWF2rAecNdkF81HvPU7vXuAgbu2fgzxYschfaFFABWQVx9+EJnxQELy4rFV7dZOmGnYpemi2Q=="
INITIATOR_NAME = "dasc"
SHORTCODE = "8286400"
FIXED_RECIPIENT = "0729149198"

# ---------------------------
# === CONFIG ===
# ---------------------------
BASE_URL = "https://sandbox.safaricom.co.ke"
CALLBACK_FILE = "callback_url.txt"
FLASK_PORT = 5000
BALANCE_CALLBACK_EVENT = threading.Event()
PARSED_BALANCE = {"amount": None}
CALLBACK_TIMEOUT_SECONDS = 60  # wait for balance callback up to this many seconds

# ---------------------------
# === Flask callback endpoints ===
# ---------------------------
@app.route("/balance_callback", methods=["POST"])
def balance_callback():
    """
    Called by Daraja (sandbox) with the AccountBalance result.
    We parse the AccountBalance parameter (string) and extract numeric amount.
    """
    data = request.get_json()
    print("\n[Callback] Raw balance callback received (debug):")
    # Keep debug print only for developer visibility in sandbox
    print(data)

    try:
        params = data["Result"]["ResultParameters"]["ResultParameter"]
        for p in params:
            if p.get("Key") == "AccountBalance":
                # Example Value: "Working Account|KES|12345.00|..."
                val = p.get("Value", "")
                parts = val.split("|")
                if len(parts) >= 3:
                    # parse numeric part
                    amount = float(parts[2].replace(",", "").strip())
                    PARSED_BALANCE["amount"] = amount
                    BALANCE_CALLBACK_EVENT.set()
                    return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"}), 200
    except Exception as e:
        print("[Callback] Parsing error:", e)

    # If parsing fails, still set event but mark None
    PARSED_BALANCE["amount"] = None
    BALANCE_CALLBACK_EVENT.set()
    return jsonify({"ResultCode": 1, "ResultDesc": "Malformed"}), 400


@app.route("/b2c_callback", methods=["POST"])
def b2c_callback():
    """
    Optional endpoint for B2C asynchronous responses (sandbox may call this).
    Print full payload for debugging.
    """
    data = request.get_json()
    print("\n[Callback] B2C callback received (debug):")
    print(data)
    return jsonify({"ResultCode": 0, "ResultDesc": "Received"}), 200

# ---------------------------
# === cloudflared quick tunnel helper ===
# ---------------------------
def start_cloudflared_and_get_url(port=FLASK_PORT, timeout=20):
    """
    Start cloudflared quick tunnel and capture the generated trycloudflare URL.
    Requires cloudflared binary to be on PATH.
    Returns (proc, public_url) or (proc, None).
    """
    cmd = ["cloudflared", "tunnel", "--url", f"http://localhost:{port}", "--no-autoupdate", "--loglevel", "info"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)

    public_url = None
    start = time.time()
    while True:
        if proc.stdout is None:
            break
        line = proc.stdout.readline()
        if not line:
            if time.time() - start > timeout:
                break
            time.sleep(0.05)
            continue
        line = line.strip()
        # Try to capture the trycloudflare URL
        m = re.search(r"https://[a-z0-9-]+\.trycloudflare\.com", line)
        if m:
            public_url = m.group(0)
            break
        if time.time() - start > timeout:
            break

    if public_url:
        with open(CALLBACK_FILE, "w") as f:
            f.write(public_url + "\n")
    return proc, public_url

# ---------------------------
# === Daraja (sandbox) helpers ===
# ---------------------------
def get_access_token_sandbox():
    url = f"{BASE_URL}/oauth/v1/generate?grant_type=client_credentials"
    r = requests.get(url, auth=(CONSUMER_KEY, CONSUMER_SECRET), timeout=20)
    r.raise_for_status()
    return r.json()["access_token"]

def call_account_balance_sandbox(access_token, result_url, timeout_url):
    url = f"{BASE_URL}/mpesa/accountbalance/v1/query"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    payload = {
        "Initiator": INITIATOR_NAME,
        "SecurityCredential": SECURITY_CREDENTIAL,
        "CommandID": "AccountBalance",
        "PartyA": SHORTCODE,
        "IdentifierType": "4",
        "Remarks": "BalanceCheck",
        "QueueTimeOutURL": timeout_url,
        "ResultURL": result_url
    }
    r = requests.post(url, json=payload, headers=headers, timeout=20)
    r.raise_for_status()
    return r.json()

def send_b2c_sandbox(access_token, amount, result_url, timeout_url):
    url = f"{BASE_URL}/mpesa/b2c/v1/paymentrequest"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    payload = {
        "InitiatorName": INITIATOR_NAME,
        "SecurityCredential": SECURITY_CREDENTIAL,
        "CommandID": "BusinessPayment",
        "Amount": int(amount),
        "PartyA": SHORTCODE,
        "PartyB": FIXED_RECIPIENT,
        "Remarks": "Sandbox sweep",
        "QueueTimeOutURL": timeout_url,
        "ResultURL": result_url,
        "Occasion": "SandboxSweep"
    }
    r = requests.post(url, json=payload, headers=headers, timeout=20)
    r.raise_for_status()
    return r.json()

# ---------------------------
# === Main orchestration ===
# ---------------------------
def main_flow():
    # 1) Start Flask server thread
    def run_flask():
        # avoid reloader to prevent double server
        app.run(host="0.0.0.0", port=FLASK_PORT, debug=False, use_reloader=False)

    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    time.sleep(0.5)

    # 2) Start cloudflared quick tunnel and get public URL
    cloud_proc, public_url = start_cloudflared_and_get_url(port=FLASK_PORT, timeout=25)
    if not public_url:
        print("❌ Could not obtain cloudflared public URL. Ensure cloudflared is installed and you have internet access.")
        return

    result_url = f"{public_url}/balance_callback"
    timeout_url = result_url
    b2c_result_url = f"{public_url}/b2c_callback"
    b2c_timeout_url = b2c_result_url

    # 3) Get access token
    try:
        token = get_access_token_sandbox()
    except Exception as e:
        print("❌ Failed to get access token:", e)
        return

    # 4) Call AccountBalance API
    try:
        bal_resp = call_account_balance_sandbox(token, result_url, timeout_url)
    except Exception as e:
        print("❌ AccountBalance API call failed:", e)
        return

    # 5) Wait for the asynchronous balance callback (strict)
    print("⏳ Waiting for balance callback (up to {}s)...".format(CALLBACK_TIMEOUT_SECONDS))
    got = BALANCE_CALLBACK_EVENT.wait(timeout=CALLBACK_TIMEOUT_SECONDS)
    if not got:
        print("❌ Timeout waiting for balance callback. Check that your ResultURL is reachable and cloudflared is running.")
        return

    amount = PARSED_BALANCE.get("amount")
    if amount is None:
        print("❌ Balance callback arrived but parsing failed. Check callback payload printed above.")
        return

    # 6) Send B2C payout with that exact amount
    try:
        b2c_resp = send_b2c_sandbox(token, amount, b2c_result_url, b2c_timeout_url)
    except Exception as e:
        print("❌ B2C API call failed:", e)
        return

    # Minimal console output
    print("\n💰 Balance detected: KES {:.2f}".format(amount))
    print("📤 B2C Response (sandbox):")
    print(b2c_resp)

    # Keep server running a short time so callbacks can arrive (you can Ctrl+C when done)
    print("\nServer still running to receive callbacks. Press Ctrl+C to stop when you have the B2C callback.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
        try:
            cloud_proc.terminate()
        except Exception:
            pass
        sys.exit(0)

# ---------------------------
# === Entrypoint / placeholder check ===
# ---------------------------
if __name__ == "__main__":
    # quick placeholder check
    placeholders = [
        CONSUMER_KEY.startswith("<"),
        CONSUMER_SECRET.startswith("<"),
        SECURITY_CREDENTIAL.startswith("<"),
        INITIATOR_NAME.startswith("<"),
        SHORTCODE.startswith("<"),
        FIXED_RECIPIENT.startswith("<")
    ]
    if any(placeholders):
        print("❌ Please edit the script and replace ALL sandbox placeholders with your sandbox credentials before running.")
        sys.exit(1)

    main_flow()
