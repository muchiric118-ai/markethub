#!/data/data/com.termux/files/usr/bin/bash
# Safaricom Certificate Manager with automatic validation + environment switcher

SANDBOX_CERT="cert_sandbox.cer"
PROD_CERT="cert_prod.cer"
ENV_FILE="active_env.conf"

validate_cert() {
    FILE=$1
    echo
    echo "🔎 Validating $FILE ..."
    if openssl x509 -inform PEM -in "$FILE" -noout -text > /dev/null 2>&1; then
        echo "✅ $FILE is a valid PEM certificate."
    else
        echo "❌ $FILE is NOT a valid certificate. Please check formatting."
    fi
    echo "------------------------------------"
}

set_env() {
    ENV=$1
    echo "$ENV" > "$ENV_FILE"
    echo "🌍 Active environment set to: $ENV"
}

get_env() {
    if [ -f "$ENV_FILE" ]; then
        cat "$ENV_FILE"
    else
        echo "sandbox"
    fi
}

echo "=============================="
echo "   Safaricom Certificate Manager"
echo "=============================="
echo "1) Edit Sandbox Certificate"
echo "2) Edit Production Certificate"
echo "3) Set Active Environment"
echo "4) Show Current Environment"
echo "5) Exit"
echo "=============================="
read -p "Choose an option [1-5]: " choice

case $choice in
  1)
    echo "Opening Sandbox certificate ($SANDBOX_CERT)..."
    [ ! -f "$SANDBOX_CERT" ] && touch "$SANDBOX_CERT"
    nano "$SANDBOX_CERT"
    validate_cert "$SANDBOX_CERT"
    ;;
  2)
    echo "Opening Production certificate ($PROD_CERT)..."
    [ ! -f "$PROD_CERT" ] && touch "$PROD_CERT"
    nano "$PROD_CERT"
    validate_cert "$PROD_CERT"
    ;;
  3)
    echo "1) Sandbox"
    echo "2) Production"
    read -p "Select environment [1-2]: " env_choice
    case $env_choice in
        1) set_env "sandbox" ;;
        2) set_env "production" ;;
        *) echo "Invalid option." ;;
    esac
    ;;
  4)
    echo "🌍 Current environment: $(get_env)"
    ;;
  5)
    echo "Exiting..."
    exit 0
    ;;
  *)
    echo "Invalid choice. Please run again."
    ;;
esac
