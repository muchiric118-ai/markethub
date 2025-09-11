import os
import json
import requests
import sqlite3
import datetime as dt
from flask import Flask, request

# =============================
# 🔐 Credentials
# =============================
BOT_TOKEN = "8438109353:AAEUGWgORF7lT7esLb-fylr4Ov8deSfq7I8"
ADMIN_ID = "1932615279"

CONSUMER_KEY = "IJbHP70UyXidTKyYdIqUC8E52CrFIcrr1DDGvmL9BKGhfKt2"
CONSUMER_SECRET = "ZcUwSvLaLKH51GO3Jqa4bwY5URfZBkd3Tioo2e4erBG9vslOGRQUf1QrmfAuDCqU"
SHORTCODE = "5185413"
PASSKEY = "dxjzlINkIxsZUDC77H61isDtafgT2oEBGMtUF7iqeUs0T0lkHRwjckysrO+mY0j7R8O59skvTrOZEGFq0PKg6UpWCDuF4wlT8IQrVhsX33UJaYzqoCY2s/3mdHmN1yEITrYtwubuO0J8XrvoR+ou5x1QlUMEH4h2tATIEL9cvbCHRqYIdlKSemKuHOsHFRF2xtqUM79uyGBA7hJ6TWYMjUjbwug4XmHYOJuCDoNjpUKQ4goziwNU/osOMCJqPyCkgGur3j9KEVX2j0L6h8a524ZxIujzZJp7u42FF1EJDHgT8ICCCA7jtMTsO0mkpTwQB3/+d6bC+3bREpmHhtu/Zw=="

# =============================
# 📦 Flask app
# =============================
app = Flask(__name__)

# =============================
# 💾 Database
# =============================
conn = sqlite3.connect("bot.db", check_same_thread=False)
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS users (chat_id TEXT PRIMARY KEY, is_vip INTEGER DEFAULT 0, last_promo TEXT)")
conn.commit()

# =============================
# ✉️ Telegram helpers
# =============================
def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

# =============================
# 🌍 Routes
# =============================
@app.route("/webhook/"+BOT_TOKEN, methods=["POST"])
def webhook():
    update = request.json
    if not update: return "No update", 400

    if "message" in update:
        chat_id = str(update["message"]["chat"]["id"])
        text = update["message"].get("text", "")

        if text.startswith("/start"):
            send_message(chat_id, "👋 Welcome! Use /services to see what we offer.")

        elif text.startswith("/services"):
            send_message(chat_id,
                "🔥 Available Services:\n"
                "1. Crypto Liquidity Access\n"
                "2. Safaricom Tools\n"
                "3. TON & Binance (coming soon)\n\n"
                "Pay easily with /pay <amount> <phone>")

        elif text.startswith("/pay"):
            send_message(chat_id, "✅ Payment request received. (Simulation for now).")

        elif text.startswith("/promo") and chat_id == ADMIN_ID:
            promo()
            send_message(chat_id, "📢 Promo sent to all users.")

        # Save user in DB
        cur.execute("INSERT OR IGNORE INTO users (chat_id) VALUES (?)", (chat_id,))
        conn.commit()

    return "ok", 200

@app.route("/health")
def health():
    return "OK", 200

# =============================
# 📢 Promo function
# =============================
def promo():
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    cur.execute("SELECT chat_id FROM users")
    for (chat_id,) in cur.fetchall():
        send_message(chat_id,
            f"🔥 Special Offer {now}:\n"
            "- Crypto liquidity deals\n"
            "- Safaricom tools\n"
            "💳 Pay via /pay <amount> <phone>")
    conn.commit()

# =============================
# 🚀 Start Flask
# =============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
