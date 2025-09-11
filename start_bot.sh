#!/data/data/com.termux/files/usr/bin/bash
# ========================================
# 🚀 Start Bot + Cloudflare (Production)
# ========================================

BOT_TOKEN="8438109353:AAEUGWgORF7lT7esLb-fylr4Ov8deSfq7I8"

echo "🔴 Stopping old processes..."
pkill -f "python3 ~/bot/bot.py"
pkill -f "cloudflared"

echo "✅ Starting bot..."
nohup python3 ~/bot/bot.py > ~/bot.log 2>&1 &

echo "🌐 Starting Cloudflare tunnel..."
nohup cloudflared tunnel --url http://127.0.0.1:8000 > ~/cloudflared.log 2>&1 &

# Wait for tunnel to initialize
sleep 8

# Extract Cloudflare URL
TUNNEL_URL=$(strings ~/cloudflared.log | grep -o "https://.*trycloudflare.com" | tail -n1)

if [ -z "$TUNNEL_URL" ]; then
    echo "❌ Failed to extract Cloudflare tunnel URL"
    exit 1
fi

echo "🌍 Tunnel URL: $TUNNEL_URL"

# Register webhook with Telegram
WEBHOOK_URL="$TUNNEL_URL/webhook/$BOT_TOKEN"
curl -s -F "url=$WEBHOOK_URL" https://api.telegram.org/bot$BOT_TOKEN/setWebhook > ~/webhook.log

echo "✅ Webhook set: $WEBHOOK_URL"
