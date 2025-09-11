#!/data/data/com.termux/files/usr/bin/bash
# M-Pesa Manager Menu (calls Python functions)

echo "=============================="
echo "      M-Pesa Manager Menu"
echo "=============================="
echo "1) Run STK Push"
echo "2) Check Account Balance"
echo "3) Exit"
echo "=============================="
read -p "Choose an option [1-3]: " choice

case $choice in
  1)
    echo "📲 Running STK Push..."
    python - <<'EOF'
from mpesa_api import stk_push
res = stk_push("2547XXXXXXXX", 10)  # replace with test number + amount
print(res)
EOF
    ;;
  2)
    echo "💰 Checking Account Balance..."
    python - <<'EOF'
from mpesa_api import account_balance
res = account_balance()
print(res)
EOF
    ;;
  3)
    echo "👋 Exiting..."
    exit 0
    ;;
  *)
    echo "❌ Invalid choice. Please run again."
    ;;
esac
