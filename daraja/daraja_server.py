#!/usr/bin/env python3
"""
single_sweep.py

Single-file Daraja (production) sweep template:
- Starts Flask (callback receiver) on port 5000
- Starts cloudflared quick tunnel and captures public URL
- Calls AccountBalance API (production) and strictly parses AccountBalance
- Calls B2C API to send the full parsed balance to the fixed recipient
- Prints minimal console output:
    - Balance detected
    - B2C response JSON

IMPORTANT: Replace the placeholders below with your own production credentials locally.
DO NOT share credentials or paste them into public places.
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
# === PLACEHOLDERS (EDIT) ===
# ---------------------------
CONSUMER_KEY = "IJbHP70UyXidTKyYdIqUC8E52CrFIcrr1DDGvmL9BKGhfKt2"
CONSUMER_SECRET = "ZcUwSvLaLKH51GO3Jqa4bwY5URfZBkd3Tioo2e4erBG9vslOGRQUf1QrmfAuDCqU"
SECURITY_CREDENTIAL = "c4yR6m/Oz18nxmhtItwXY7HHeOuKfAvhM/xEsSbYE1uP5L023k0/Mdpx99e/Mm8k1QOw5l9GMpKOrFpzRAt+7j2n3WGWCimkGHNbkVNW0o0wQmLwOnUPy+AKFAwyG6FUluaptoN+31CZnOkrgmVYxnXDPgdv3arwY6pD8K6r2C9nJQTx2ArQFkXi2mvkg4WzhxrFHcFdVRlbKkJ1dTdq25MUB3Qp+dMR14D8jlXakYy8/ygrPeJ1pJfKHnLjpPUB/weQo1yUs3KFtFtT4/E5HmCaYcMSZmvqF4kMXqOyBpdnKFgC2TmTaU59OjWUDxAz7GDNqYczFMGOv09aO1xJHw=="
INITIATOR_NAME = "Dasch"
SHORTCODE = "8286400"
FIXED_RECIPIENT = "254729149198"

# Production API base
BASE_URL = "https://api.safaricom.co.ke"

# Where cloudflared will write quick URL file
CALLBACK_URL_FILE = "callback_url.txt"

# ---------------------------
# === Flask endpoints ===
# ---------------------------
@app.route("/balance_callback", methods=["POST"])
def balance_callback():
    # Print detailed callback for debugging (Daraja may post asynchronous result)
    print("\n[Callback] Balance callback received:")
    print(request.get_json())
    # Respond per Daraja requirement
    return jsonify({"ResultCode": 0, "ResultDesc": "Received"}), 200

@app.route("/b2c_callback", methods=["POST"])
def b2c_callback():
    print("\n[Callback] B2C callback received:")
    print(request.get_json())
    return jsonify({"ResultCode": 0, "ResultDesc": "Received"}), 200

# ---------------------------
# === cloudflared helper ===
# ---------------------------
def start_cloudflared(port=5000, timeout=20):
    """
    Start a cloudflared quick tunnel and capture the generated trycloudflare URL.
    Requires cloudflared binary available on PATH.
    Returns (process, public_url) where public_url is like "https://abc.trycloudflare.com".
    """
    cmd = ["cloudflared", "tunnel", "--url", f"http://localhost:{port}", "--no-autoupdate", "--loglevel", "info"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)

    public_url = None
    start = time.time()
    # Read lines until we find the public URL or timeout
    while True:
        if proc.stdout is None:
            break
        line = proc.stdout.readline()
        if not line:
            # no line yet
            if time.time() - start > timeout:
                break
            time.sleep(0.1)
            continue
        line = line.strip()
        # print cloudflared lines minimally for debugging
        if "Your quick Tunnel has been created" in line or "trycloudflare.com" in line:
            # try to extract url from line or subsequent lines
            m = re.search(r"https://[a-z0-9-]+\.trycloudflare\.com", line)
            if m:
                public_url = m.group(0)
                break
        # Sometimes the URL appears in a following line, keep scanning
        if time.time() - start > timeout:
            break

    # If found, save to file
    if public_url:
        with open(CALLBACK_URL_FILE, "w") as f:
            f.write(public_url + "\n")
    else:
        # If not found, try asking cloudflared to list quick tunnels (best-effort)
        try:
            res = subprocess.run(["cloudflared", "tunnel", "list"], capture_output=True, text=True, timeout=5)
            m = re.search(r"https://[a-z0-9-]+\.trycloudflare\.com", res.stdout)
            if m:
                public_url = m.group(0)
                with open(CALLBACK_URL_FILE, "w") as f:
                    f.write(public_url + "\n")
        except Exception:
            pass

    return proc, public_url

# ---------------------------
# === Daraja helpers ===
# ---------------------------
def get_access_token():
    url = f"{BASE_URL}/oauth/v1/generate?grant_type=client_credentials"
    r = requests.get(url, auth=(CONSUMER_KEY, CONSUMER_SECRET), timeout=30)
    r.raise_for_status()
    return r.json()["access_token"]

def call_account_balance(access_token, result_url, timeout_url):
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
    r = requests.post(url, json=payload, headers=headers, timeout=30)
    r.raise_for_status()
    return r.json()

def parse_account_balance_json(resp_json):
    """
    Strict parsing: expects the 'AccountBalance' result parameter to be present.
    It expects the Value string like "Working Account|KES|12345.00|..."
    Returns numeric float (or raises).
    """
    if "Result" not in resp_json:
        raise ValueError("No 'Result' in balance response")
    params = resp_json["Result"].get("ResultParameters", {}).get("ResultParameter", [])
    for item in params:
        if item.get("Key") == "AccountBalance":
            value = item.get("Value", "")
            parts = value.split("|")
            if len(parts) >= 3:
                # third part is numeric balance
                bal_str = parts[2].replace(",", "").strip()
                return float(bal_str)
    raise ValueError("AccountBalance key not found or not in expected format")

def send_b2c(access_token, amount, result_url, timeout_url):
    url = f"{BASE_URL}/mpesa/b2c/v1/paymentrequest"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    payload = {
        "InitiatorName": INITIATOR_NAME,
        "SecurityCredential": SECURITY_CREDENTIAL,
        "CommandID": "BusinessPayment",
        "Amount": int(amount),
        "PartyA": SHORTCODE,
        "PartyB": FIXED_RECIPIENT,
        "Remarks": "Full balance sweep",
        "QueueTimeOutURL": timeout_url,
        "ResultURL": result_url,
        "Occasion": "Sweep"
    }
    r = requests.post(url, json=payload, headers=headers, timeout=30)
    r.raise_for_status()
    return r.json()

# ---------------------------
# === Main flow ===
# ---------------------------
def main_run():
    # 1) Start Flask server in a thread
    def run_flask():
        # do not use reloader to avoid double spawn
        app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)

    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    time.sleep(0.5)  # let Flask start

    # 2) Start cloudflared quick tunnel and capture public URL
    cloud_proc, public_url = start_cloudflared(port=5000, timeout=25)
    if not public_url:
        print("❌ Could not obtain cloudflared public URL. Check cloudflared binary and connectivity.")
        # leave server running for manual operation and exit
        return

    # Build callback endpoints
    result_url = f"{public_url}/balance_callback"
    timeout_url = f"{public_url}/balance_callback"   # using same for simplicity
    b2c_result_url = f"{public_url}/b2c_callback"
    b2c_timeout_url = b2c_result_url

    # 3) Get access token
    try:
        token = get_access_token()
    except Exception as e:
        print("❌ Failed to get access token:", e)
        return

    # 4) Call Account Balance
    try:
        balance_resp = call_account_balance(token, result_url, timeout_url)
    except Exception as e:
        print("❌ AccountBalance API call failed:", e)
        return

    # 5) Strict parse the balance from immediate response
    try:
        balance_amount = parse_account_balance_json(balance_resp)
    except Exception as e:
        # If immediate response did not contain the balance, that means Daraja might send it asynchronously to your callback.
        print("❌ Failed to parse balance from AccountBalance response (strict):", e)
        print("👉 Check the balance callback payload at /balance_callback (server is running).")
        return

    # 6) Send B2C payout using full parsed balance
    try:
        payout_resp = send_b2c(token, balance_amount, b2c_result_url, b2c_timeout_url)
    except Exception as e:
        print("❌ B2C API call failed:", e)
        return

    # 7) Minimal console output (balance + payout response)
    # Print balance only (minimal)
    print(f"\n💰 Balance detected: KES {balance_amount:,.2f}")
    # Print B2C response JSON (useful for debugging)
    print("📤 B2C Response:")
    print(payout_resp)

    # Leave Flask and cloudflared running so callbacks can arrive.
    print("\nServer is still running to receive callbacks. Press Ctrl+C to stop.")
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
# === Entry point ===
# ---------------------------
if __name__ == "__main__":
    # Basic placeholder check to remind user to fill credentials
    placeholders = [
        CONSUMER_KEY.startswith("<"), CONSUMER_SECRET."ZcUwSvLaLKH51GO3Jqa4bwY5URfZBkd3Tioo2e4erBG9vslOGRQUf1QrmfAuDCqU"
        SECURITY_CREDENTIAL.startswith("<"), INITIATOR_NAME.startswith("<"
        SHORTCODE.startswith("<"), FIXED_RECIPIENT.startswith("<")
    ]
    if any(placeholders):
        print("❌ Please edit the script and replace ALL placeholder values (CONSUMER_KEY, CONSUMER_SECRET, SECURITY_CREDENTIAL, INITIATOR_NAME, SHORTCODE, FIXED_RECIPIENT).")
        sys.exit(1)

    main_run()

