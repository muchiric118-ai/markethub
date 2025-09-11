#!/data/data/com.termux/files/usr/bin/bash
# Script to open/edit the Safaricom Production certificate in nano

CERT_FILE="cert_prod.cer"

# If the cert file does not exist, create it
if [ ! -f "$CERT_FILE" ]; then
    echo "Creating new production certificate file: $CERT_FILE"
    touch "$CERT_FILE"
fi

# Open the cert file in nano
nano "$CERT_FILE"
