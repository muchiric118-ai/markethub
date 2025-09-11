#!/data/data/com.termux/files/usr/bin/sh
echo "🔴 Stopping all Gunicorn and Cloudflared processes..."

# Kill Gunicorn
ps -aux | grep gunicorn | grep -v grep | awk '{print $2}' | xargs -r kill -9

# Kill Cloudflared
ps -aux | grep cloudflared | grep -v grep | awk '{print $2}' | xargs -r kill -9

echo "✅ All old processes stopped. Ready to start fresh."
