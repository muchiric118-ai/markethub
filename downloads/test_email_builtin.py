import smtplib
from email.mime.text import MIMEText

# Replace with your details
SENDER_EMAIL = "your_email@gmail.com"
APP_PASSWORD = "your_16_char_app_password"
RECEIVER_EMAIL = "your_email@gmail.com"

try:
    # Create the email
    msg = MIMEText("Hello! This is a test email from Termux using smtplib.")
    msg["Subject"] = "✅ Test Email from Termux"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL

    # Connect to Gmail SMTP
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(SENDER_EMAIL, txqj vazx rhng fznaD)
    server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
    server.quit()

    print("📧 Test email sent successfully with smtplib!")
except Exception as e:
    print(f"❌ Failed to send email: {e}")
