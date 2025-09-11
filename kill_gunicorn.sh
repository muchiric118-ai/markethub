#!/data/data/com.termux/files/usr/bin/sh
echo "🔴 Killing all Gunicorn processes..."
ps -aux | grep gunicorn | grep -v grep | awk '{print $2}' | xargs -r kill -9
echo "✅ Done. All Gunicorn processes stopped."
