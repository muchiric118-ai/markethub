echo "🌍 Public URL: $url"
echo "$(date) - $url" >> ~/cloudflared_urls.txt

# Telegram config
BOT_TOKEN="8438109353:AAEUGWgORF7lT7esLb-fylr4Ov8deSfq7I8"
CHAT_ID="1923615279"

# Avoid duplicate messages: check last sent URL
LAST_URL_FILE=~/last_url.txt
if [ ! -f "$LAST_URL_FILE" ] || [ "$url" != "$(cat $LAST_URL_FILE)" ]; then
    echo "$url" > $LAST_URL_FILE
    curl -s -X POST https://api.telegram.org/bot$BOT_TOKEN/sendMessage \
        -d chat_id=$CHAT_ID \
        -d text="🌍 New cloudflared URL: $url"
fi

