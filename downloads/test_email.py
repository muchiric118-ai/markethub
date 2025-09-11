import yagmail

# Replace with your details
SENDER_EMAIL = "your_email@gmail.com"
APP_PASSWORD = "your_16_char_app_password"
RECEIVER_EMAIL = "your_email@gmail.com"  # or any other email to receive the test

try:
    # Connect to Gmail
    yag = yagmail.SMTP(SENDER_EMAIL, APP_PASSWORD)

    # Send a test email
    subject = "✅ Test Email from Termux"
    body = "Hello! This is a test email from your Termux + Python setup."
    yag.send(RECEIVER_EMAIL, subject, body)

    print("📧 Test email sent successfully!")
except Exception as e:
    print(f"❌ Failed to send email: {e}")
