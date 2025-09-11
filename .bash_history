mkdir ~/daraja
cd ~/daraja
mkdir ~/daraja
cd ~/daraja
nano daraja_server.py
python daraja_server.py
lsof -i :5000
ss -ltnp | grep 5000
pkg install iproute2 -y
ss -ltnp | grep 5000
pkill -f python
cd ~/daraja
python daraja_server.py
python daraja_server_with_tunnel.py
cd ~/daraja
nano daraja_server_with_tunnel.py
python daraja_server_with_tunnel.py
cloudflared tunnel --url http://localhost:5000 --no-autoupdate --loglevel info
python daraja_server.py
python ~/daraja/daraja_server.py
nano daraja_server.py
python daraja_auto_sandbox.py
cd ~/daraja
nano daraja_auto_sandbox.py
python daraja_auto_sandbox.py
nano daraja_auto_sandbox.py
python daraja_auto.py
araja $ python daraja_auto.py                  python: can't open file '/data/data/com.termux/files/home/daraja/daraja_auto.py': [Errno 2] No such file or directory                                 ~/daraja $
# Create a 2 GB swap file
dd if=/dev/zero of=$HOME/swapfile bs=1M count=2048
# Set it up as swap
mkswap $HOME/swapfile
# Enable it
swapon $HOME/swapfile
pkg install util-linux procps
which mkswap
which swapon
The program which is not installed. Install it by executing:
which mkswap
which swapon
pkg install mount-utils blkid
pkg install e2fsprogs mount-utils
Unpacking mount-utils (2.40.2-5) ...
Setting up libblkid (2.40.2-5) ...
Setting up libmount (2.40.2-5) ...
Setting up e2fsprogs (1.47.3) ...
Setting up mount-utils (2.40.2-5) ...
~/gophish $
which mkswap
which swapon
pkg install util-linux
# Create a 2GB swap file
dd if=/dev/zero of=$HOME/swapfile bs=1M count=2048
# Enable swap without mkswap
swapon $HOME/swapfile
# Check if it’s active
free -h
cd ~/gophish
GOMAXPROCS=2 go build -v -o gophish gophish.go
ls -lh ~/gophish/gophish
# Give correct permissions
chmod 600 $HOME/swapfile
# Initialize swap header
mkswap $HOME/swapfile
# Enable swap
swapon $HOME/swapfile
pkg install blk-utils
# Secure file permissions
chmod 600 $HOME/swapfile
# Write swap header
mkswap $HOME/swapfile
# Enable swap
swapon $HOME/swapfile
# Verify
free -h
echo "chmod 600 $HOME/swapfile && mkswap $HOME/swapfile && swapon $HOME/swapfile" >> $HOME/.bashrc
cd ~/gophish
nano config.json
./gophish
nano ~/gophish/config.json
./gophish
cd ~/gophish
./gophish
nano ~/gophish/config.json
cd ~/gophish
./gophish
#!/bin/bash
# Start cloudflared tunnel in background
nohup cloudflared tunnel --url https://localhost:9443 > ~/cloudflared.log 2>&1 &
# Wait a bit for it to start
sleep 3
# Check if process is running
if pgrep -x "cloudflared" > /dev/null; then     echo "✅ cloudflared is running."; 
    url=$(grep -o 'https://[-0-9a-z]*\.trycloudflare.com' ~/cloudflared.log | tail -n 1);      if [ -n "$url" ]; then         echo "🌍 Public URL: $url";     else         echo "⚠️ Could not find public URL yet. Check ~/cloudflared.log";     fi; else     echo "❌ cloudflared failed to start. Check ~/cloudflared.log"; fi
#!/bin/bash
# Start cloudflared tunnel in background
nohup cloudflared tunnel --url https://localhost:9443 > ~/cloudflared.log 2>&1 &
# Wait a bit for it to start
sleep 3
# Check if process is running
if pgrep -x "cloudflared" > /dev/null; then     echo "✅ cloudflared is running."; 
    url=$(grep -o 'https://[-0-9a-z]*\.trycloudflare.com' ~/cloudflared.log | tail -n 1);      if [ -n "$url" ]; then         echo "🌍 Public URL: $url";     else         echo "⚠️ Could not find public URL yet. Check ~/cloudflared.log";     fi; else     echo "❌ cloudflared failed to start. Check ~/cloudflared.log"; fi
# Start cloudflared tunnel in background
nohup cloudflared tunnel --url https://localhost:9443 > ~/cloudflared.log 2>&1 &
# Wait a bit for process to spin up
sleep 2
# Check if process is running
if pgrep -x "cloudflared" > /dev/null; then     echo "✅ cloudflared is running. Waiting for public URL..."; 
    for i in {1..30}; do         url=$(grep -o 'https://[-0-9a-z]*\.trycloudflare.com' ~/cloudflared.log | tail -n 1);         if [ -n "$url" ]; then             echo "🌍 Public URL: $url";             exit 0;         fi;         sleep 1;     done;      echo "⚠️ Timed out waiting for public URL. Check ~/cloudflared.log"; else     echo "❌ cloudflared failed to start. Check ~/cloudflared.log"
#!/bin/bash
# Start cloudflared tunnel in background
nohup cloudflared tunnel --url https://localhost:9443 > ~/cloudflared.log 2>&1 &
# Wait a bit for process to spin up
sleep 2
# Check if process is running
if pgrep -x "cloudflared" > /dev/null; then     echo "✅ cloudflared is running. Waiting for public URL..."; 
    for i in {1..30}; do         url=$(grep -o 'https://[-0-9a-z]*\.trycloudflare.com' ~/cloudflared.log | tail -n 1);         if [ -n "$url" ]; then             echo "🌍 Public URL: $url";             exit 0;         fi;         sleep 1;     done;      echo "⚠️ Timed out waiting for public URL. Check ~/cloudflared.log"; else     echo "❌ cloudflared failed to start. Check ~/cloudflared.log"; fi
grep -a -o 'https://[-0-9a-z]*\.trycloudflare.com' ~/cloudflared.log | tail -n 1
#!/bin/bash
# Start cloudflared tunnel in background
nohup cloudflared tunnel --url https://localhost:9443 > ~/cloudflared.log 2>&1 &
# Wait a bit for process to spin up
sleep 2
# Check if process is running
if pgrep -x "cloudflared" > /dev/null; then     echo "✅ cloudflared is running. Waiting for public URL..."; 
    for i in {1..30}; do         url=$(grep -a -o 'https://[-0-9a-z]*\.trycloudflare.com' ~/cloudflared.log | tail -n 1);         if [ -n "$url" ]; then             echo "🌍 Public URL: $url";             exit 0;         fi;         sleep 1;     done;      echo "⚠️ Timed out waiting for public URL. Check ~/cloudflared.log"; else     echo "❌ cloudflared failed to start. Check ~/cloudflared.log"; fi
cloudflared tunnel --url https://0.0.0.0:9443
nohup cloudflared tunnel --url https://localhost:9443 > cloudflared.log 2>&1 &
ps -aux | grep cloudflared
pkill -f cloudflared
nohup cloudflared tunnel --url https://localhost:9443 > ~/cloudflared.log 2>&1 &
ps -aux | grep cloudflared
nohup cloudflared tunnel --url https://localhost:9443 > ~/cloudflared.log 2>&1 &
ps -aux | grep cloudflared
#!/bin/bash
# Kill any existing cloudflared processes
if pgrep -x "cloudflared" > /dev/null; then     echo "🛑 Stopping existing cloudflared...";     pkill -x cloudflared;     sleep 2; fi
# Start new cloudflared tunnel in background
echo "🚀 Starting cloudflared..."
nohup cloudflared tunnel --url https://localhost:9443 > ~/cloudflared.log 2>&1 &
# Wait a bit for process to spin up
sleep 2
# Check if process is running
if pgrep -x "cloudflared" > /dev/null; then     echo "✅ cloudflared is running. Waiting for public URL..."; 
    for i in {1..30}; do         url=$(grep -a -o 'https://[-0-9a-z]*\.trycloudflare.com' ~/cloudflared.log | tail -n 1);         if [ -n "$url" ]; then             echo "🌍 Public URL: $url";             exit 0;         fi;         sleep 1;     done;      echo "⚠️ Timed out waiting for public URL. Check ~/cloudflared.log"; else     echo "❌ cloudflared failed to start. Check ~/cloudflared.log"; fi
#!/bin/bash
LOG=~/cloudflared.log
# Function to start cloudflared
start_cloudflared() {     echo "🚀 Starting cloudflared...";     nohup cloudflared tunnel --url https://localhost:9443 > "$LOG" 2>&1 &     sleep 2; }
# Function to get public URL
get_url() {     grep -a -o 'https://[-0-9a-z]*\.trycloudflare.com' "$LOG" | tail -n 1; }
# Kill any old processes first
if pgrep -x "cloudflared" > /dev/null; then     echo "🛑 Stopping old cloudflared...";     pkill -x cloudflared;     sleep 2; fi
# Watchdog loop
while true; do
    start_cloudflared; 
    echo "⏳ Waiting for public URL...";     for i in {1..30}; do         url=$(get_url);         if [ -n "$url" ]; then             echo "🌍 Public URL: $url";             break;         fi;         sleep 1;     done; 
    while pgrep -x "cloudflared" > /dev/null; do         sleep 5;     done;      echo "⚠️ cloudflared crashed
~ $ curl -s https://api.telegram.org/bot<curl -s https://api.telegram.org/bot8438109353:AAEUGWgORF7lT7esLb-fylr4Ov8deSfq7I8/getUpdates
pkg update -y && pkg install curl -y
curl -s https://api.telegram.org/bot8438109353:AAEUGWgORF7lT7esLb-fylr4Ov8deSfq7I8/getUpdates
nano ~/cloudflared_watchdog.sh
curl -s -X POST "https://api.telegram.org/bot8438109353:AAEUGWgORF7lT7esLb-fylr4Ov8deSfq7I8/sendMessage"     -d chat_id=1923615279     -d text="✅ Test: Your Termux bot is working!
curl -s -X POST "https://api.telegram.org/bot8438109353:AAEUGWgORF7lT7esLb-fylr4Ov8deSfq7I8/sendMessage"     -d chat_id=1923615279     -d text="✅ Test: Your Termux bot is working!"
pkill -f python
pkill -f cloudflared
python bot.py
cd ~/tg-mpesa-bot
ls
cd ~/downloads
nano bot.py
pkg update && pkg upgrade -y
pkg install python git wget nano -y
pip install python-telegram-bot==20.3 requests flask apscheduler
cd ~/downloads
nano bot.py
nano ~/bot/start.sh
...ata/com.termux/files/home/bot/start.sh Modified
#!/data/data/com.termux/files/usr/bin/bash
# Start Supervisor with custom config
CONFIG=~/.config/supervisord.conf
if [ ! -f "$CONFIG" ]; then   echo "Supervisor config not found at $CONFIG";   exit 1; fi
# Kill all Python (bot) processes
pkill -f python3
# Kill all Cloudflare tunnel processes
pkill -f cloudflared
ps -aux | grep python
ps -aux | grep cloudflared
exit
nohup cloudflared tunnel --url http://127.0.0.1:8000 > ~/cloudflared.log 2>&1 &
strings ~/cloudflared.log | grep trycloudflare.com
pkill -f python
pkill -f gunicorn
pkill -f cloudflared
exit
nano ~/start_bot.sh
chmod +x ~/start_bot.sh
~/start_bot.sh
nano ~/bot/app.py
nano ~/start_bot.sh
chmod +x ~/start_bot.sh
~/start_bot.sh
nano ~/start_bot.sh
chmod +x ~/start_bot.sh
~/start_bot.sh
strings ~/cloudflared.log | grep trycloudflare.com
curl -i https://guaranteed-apply-alexander-west.trycloudflare.com/health
curl -F "url=https://guaranteed-apply-alexander-west.trycloudflare.com/webhook/8438109353:AAEUGWgORF7lT7esLb-fylr4Ov8deSfq7I8" https://api.telegram.org/bot8438109353:AAEUGWgORF7lT7esLb-fylr4Ov8deSfq7I8/setWebhook
nano ~/start_bot.sh
chmod +x ~/start_bot.sh
~/start_bot.sh
/bot $ ~/start_bot.sh
🔴 Stopping old processes...
✅ Starting bot...
🌐 Starting Cloudflare tunnel...
❌ Failed to extract Cloudflare tunnel URL
/bot $ ~/start_bot.sh
🔴 Stopping old processes...
✅ Starting bot...
🌐 Starting Cloudflare tunnel...
❌ Failed to extract Cloudflare tunnel URL
nano ~/start_bot.sh
~/reset_bot.sh
nano ~/bot/bot.py
pkill -f cloudflared
pkill -f bot.py
nohup python3 ~/bot/bot.py > ~/bot.log 2>&1 &
nohup cloudflared tunnel --url http://127.0.0.1:8000 > ~/cloudflared.log 2>&1 &
nano ~/start_bot.sh
mkdir -p ~/.termux/boot/
nano ~/.termux/boot/start.sh
chmod +x ~/.termux/boot/start.sh
~/.termux/boot/start.sh
nano ~/bot/bot.py
chmod +x ~/start_bot.sh
~/start_bot.sh
nano ~/start_bot.sh
ls ~/bot/bot.py
chmod +x ~/start_bot.sh
~/start_bot.sh
strings ~/bot/cloudflared.log | grep trycloudflare.com
curl -i https://voip-rider-searches-chi.trycloudflare.com/health
pkill -f python
pkill -f gunicorn
pkill -f cloudflared
nohup python3 ~/bot/bot.py > ~/bot.log 2>&1 &
ps -aux | grep python
nohup python3 ~/bot/bot.py > ~/bot.log 2>&1 &
ps -aux | grep python
tail -n 50 ~/bot.log
nano ~/bot/bot.py
pkill -f bot.py
pkill -f cloudflared
nohup python3 ~/bot/bot.py > ~/bot.log 2>&1 &
nohup cloudflared tunnel --url http://127.0.0.1:8000 > ~/cloudflared.log 2>&1 &
strings ~/cloudflared.log | grep trycloudflare.com
curl -F "url=https://fault-gsm-nominations-heart.trycloudflare.com/webhook/8438109353:AAEUGWgORF7lT7esLb-fylr4Ov8deSfq7I8" https://api.telegram.org/bot8438109353:AAEUGWgORF7lT7esLb-fylr4Ov8deSfq7I8/setWebhook
exit
cd ~/bot
~/.local/bin/honcho start
FO] Worker exiting (pid: 18325)
09:33:23 bot.1  | [2025-09-08 09:33:23 +0300] [17536] [INFO] Shutting down: Master
09:33:23 system | bot.1 stopped (rc=0)
nano ~/bot/bot.py
pkill -f bot.py
pkill -f cloudflared
nohup python3 ~/bot/bot.py > ~/bot.log 2>&1 &
ps -aux | grep bot.py
nohup cloudflared tunnel --url http://127.0.0.1:8000 > ~/cloudflared.log 2>&1 &
strings ~/cloudflared.log | grep trycloudflare.com
curl -F "url=https://cleared-better-hostels-ultram.trycloudflare.com/webhook/8438109353:AAEUGWgORF7lT7esLb-fylr4Ov8deSfq7I8" https://api.telegram.org/bot8438109353:AAEUGWgORF7lT7esLb-fylr4Ov8deSfq7I8/setWebhook
nano ~/bot/bot.py
rm -rf ~/bot
rm -f ~/start_bot.sh
rm -f ~/.termux/boot/start.sh
mkdir ~/bot
cd ~/bot
nano ~/bot/bot.py
nano ~/start_bot.sh
chmod +x ~/start_bot.sh
~/start_bot.sh
tail -n 30 ~/bot.log
nohup python3 ~/bot/bot.py > ~/bot.log 2>&1 &
nohup cloudflared tunnel --url http://127.0.0.1:8000 > ~/cloudflared.log 2>&1 &
strings ~/cloudflared.log | grep trycloudflare.com
tail -n 50 ~/bot.log
lsof -i :8000
kill -9 <PID>
ps -aux | grep 8000
lsof -i :8000
netstat -anp | grep 8000
ps -aux | grep python
kill -9 20338
nohup python3 ~/bot/bot.py > ~/bot.log 2>&1 &
nohup cloudflared tunnel --url http://127.0.0.1:8000 > ~/cloudflared.log 2>&1 &
ps -aux | grep bot.py
strings ~/cloudflared.log | grep trycloudflare.com
curl -F "url=https://impossible-eng-korea-meets.trycloudflare.com/webhook/8438109353:AAEUGWgORF7lT7esLb-fylr4Ov8deSfq7I8" https://api.telegram.org/bot8438109353:AAEUGWgORF7lT7esLb-fylr4Ov8deSfq7I8/setWebhook
nano ~/start_bot.sh
chmod +x ~/start_bot.sh
~/start_bot.sh
exit
strings ~/cloudflared.log | grep trycloudflare.com
curl -F "url=https://lucy-prague-lodging-limitations.trycloudflare.com/webhook/8438109353:AAEUGWgORF7lT7esLb-fylr4Ov8deSfq7I8" https://api.telegram.org/bot8438109353:AAEUGWgORF7lT7esLb-fylr4Ov8deSfq7I8/setWebhook
curl https://api.telegram.org/bot8438109353:AAEUGWgORF7lT7esLb-fylr4Ov8deSfq7I8/getWebhookInfo
nohup cloudflared tunnel --url http://127.0.0.1:8000 > ~/cloudflared.log 2>&1 &
strings ~/cloudflared.log | grep trycloudflare.com
curl -F "url=https://NEWURL.trycloudflare.com/webhook/8438109353:AAEUGWgORF7lT7esLb-fylr4Ov8deSfq7I8" https://api.telegram.org/bot8438109353:AAEUGWgORF7lT7esLb-fylr4Ov8deSfq7I8/setWebhook
pkill -f cloudflared
curl -F "url=https://image-tracy-replied-accommodate.trycloudflare.com/webhook/8438109353:AAEUGWgORF7lT7esLb-fylr4Ov8deSfq7I8" https://api.telegram.org/bot8438109353:AAEUGWgORF7lT7esLb-fylr4Ov8deSfq7I8/setWebhook
curl https://api.telegram.org/bot8438109353:AAEUGWgORF7lT7esLb-fylr4Ov8deSfq7I8/getWebhookInfo
nohup cloudflared tunnel --url http://127.0.0.1:8000 > ~/cloudflared.log 2>&1 &
strings ~/cloudflared.log | grep trycloudflare.com
~/reset_bot.sh
exit
nano ~/reset_bot.sh
chmod +x ~/reset_bot.sh
~/reset_bot.sh
cd ~/bot
~/.local/bin/honcho start
pkill -f gunicorn
pkill -f cloudflared
cd ~/bot && ~/.local/bin/honcho start
nano ~/bot/start_all.sh
chmod +x ~/bot/start_all.sh
~/bot/start_all.sh
nano ~/bot/watchdog.sh
chmod +x ~/bot/watchdog.sh
pkg install cronie -y
crond
crontab -e
~/bot/start_all.sh
strings ~/cloudflared.log | grep trycloudflare.com
pkill -f cloudflared
nohup cloudflared tunnel --url http://127.0.0.1:8000 > ~/cloudflared.log 2>&1 &
strings ~/cloudflared.log | grep trycloudflare.com
curl https://api.telegram.org/bot8438109353:AAEUGWgORF7lT7esLb-fylr4Ov8deSfq7I8/getWebhookInfo
curl -X POST http://127.0.0.1:8000/webhook/8438109353:AAEUGWgORF7lT7esLb-fylr4Ov8deSfq7I8 -H "Content-Type: application/json" -d '{"test":"hello"}'
nano ~/bot/bot.py
cd ~/bot
~/.local/bin/honcho start
pkill -f gunicorn
ps -aux | grep gunicorn
kill -9 <PID>
nano ~/kill_gunicorn.sh
chmod +x ~/kill_gunicorn.sh
nano ~/reset_all.sh
chmod +x ~/reset_all.sh
~/reset_all.sh
cd ~/bot
~/.local/bin/honcho start
@app.route("/health", methods=["GET"])
def health():
nano ~/bot/bot.py
cat ~/bot/bot.py | head -n 40
nano ~/reset_bot.sh
chmod +x ~/reset_bot.sh
~/reset_bot.sh
cd ~/bot
~/.local/bin/honcho start
nano ~/bot/bot.py
pkill -f gunicorn
pkill -f cloudflared
nano ~/bot/bot.py
cd ~/bot
~/.local/bin/honcho start
nano ~/reset_bot.sh
chmod +x ~/reset_bot.sh
~/reset_bot.sh
chmod +x ~/reset_bot.sh
~/reset_bot.sh
nano ~/reset_bot.sh
chmod +x ~/start_bot.sh
nano ~/start_bot.sh
chmod +x ~/start_bot.sh
~/start_bot.sh
exit
# Update Termux, install core build tools
pkg update -y && pkg upgrade -y && pkg install python clang libffi openssl rust cargo git wget curl -y
# Set up project folder
mkdir -p ~/liquidity_engine && cd ~/liquidity_engine
# Create Python virtualenv
python -m virtualenv .venv
source .venv/bin/activate
# Upgrade pip safely
pip install --upgrade pip --no-warn-script-location
# Install Python dependencies (lighter pinned CCXT)
pip install fastapi uvicorn ccxt==2.9.20 python-dotenv sqlite-utils requests aiohttp pandas plotly
# Optional: Rust-Python performance layer (PyO3)
cargo install --locked --root ~/.cargo maturin || echo "maturin already cached"
maturin init --bindings pyo3
maturin develop
# Create helper script for fast rebuild & test
echo -e '#!/bin/bash\nsource ~/liquidity_engine/.venv/bin/activate\nmaturin develop\npython -c "from liquidity_api import *; print(\"Liquidity Engine Ready\")"' > run.sh
chmod +x run.sh
exit
