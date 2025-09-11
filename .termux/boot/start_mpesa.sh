#!/data/data/com.termux/files/usr/bin/bash
cd /data/data/com.termux/files/home   # Go to home directory

# Create a logs folder if it doesn’t exist
mkdir -p logs

# Start Flask + ngrok inside tmux, logging everything
tmux new -d -s mpesa "python mpesa_app.py | tee logs/server.log"#!/data/data/com.termux/files/usr/bin/bash
cd /data/data/com.termux/files/home   # Go to home
tmux new -d -s mpesa "python mpesa_app.py"
