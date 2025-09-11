# create_env.py

def create_env_file():
    print("Let's create your .env file for Gmail SMTP.\n")

    sender = input("Enter your Gmail address: ").strip()
    password = input("Enter your Gmail App Password (16 characters): ").strip()
    receiver = input("Enter recipient email address: ").strip()

    content = (
        f"SENDER_EMAIL={sender}\n"
        f"GMAIL_APP_PASSWORD={password}\n"
        f"RECEIVER_EMAIL={receiver}\n"
    )

    with open(".env", "w") as f:
        f.write(content)

    print("\n✅ .env file created successfully!")

if __name__ == "__main__":
    create_env_file()
# create_env.py
import getpass

def create_env_file():
    print("Let's create your .env file for Gmail SMTP.\n")

    sender = input("Enter your Gmail address: ").strip()
    # getpass hides the password while typing
    password = getpass.getpass("Enter your Gmail App Password (16 characters): ").strip()
    receiver = input("Enter recipient email address: ").strip()

    content = (
        f"SENDER_EMAIL={sender}\n"
        f"GMAIL_APP_PASSWORD={password}\n"
        f"RECEIVER_EMAIL={receiver}\n"
    )

    with open(".env", "w") as f:
        f.write(content)

    print("\n✅ .env file created successfully!")

if __name__ == "__main__":
    create_env_file()
#!/usr/bin/env python3
"""
Email Tool - Send emails via Gmail and manage logs.
Features:
- Send emails (TO, CC, BCC, attachments, HTML/plain)
- Logs with unique Email IDs
- Search logs by ID, Subject, or Date
"""

import os
import smtplib
import datetime
import uuid
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

LOG_FILE = "email_log.txt"

# Load .env variables
load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

TO_EMAILS = os.getenv("TO_EMAILS", "").split(",") if os.getenv("TO_EMAILS") else []
CC_EMAILS = os.getenv("CC_EMAILS", "").split(",") if os.getenv("CC_EMAILS") else []
BCC_EMAILS = os.getenv("BCC_EMAILS", "").split(",") if os.getenv("BCC_EMAILS") else []

TO_EMAILS = [email.strip() for email in TO_EMAILS if email.strip()]
CC_EMAILS = [email.strip() for email in CC_EMAILS if email.strip()]
BCC_EMAILS = [email.strip() for email in BCC_EMAILS if email.strip()]
all_recipients = TO_EMAILS + CC_EMAILS + BCC_EMAILS


def send_email():
    """Compose and send a new email."""
    subject = input("Enter email subject: ").strip()

    use_file = input("Load body from file? (y/n): ").strip().lower() == "y"
    if use_file:
        file_path = input("Enter path to file (e.g., template.html or message.txt): ").strip()
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                body = f.read()
            print(f"📄 Loaded email body from: {file_path}")
        else:
            print(f"⚠️ File not found, defaulting to manual input.")
            body = input("Enter email body: ").strip()
    else:
        body = input("Enter email body: ").strip()

    send_html = input("Do you want to send as HTML? (y/n): ").strip().lower() == "y"

    attachments_input = input("Enter attachment file paths (comma-separated, leave blank if none): ").strip()
    attachments = [a.strip() for a in attachments_input.split(",") if a.strip()]

    # ---------- Preview ----------
    print("\n================= 📧 EMAIL PREVIEW =================")
    print(f"From: {SENDER_EMAIL}")
    print(f"To: {', '.join(TO_EMAILS) if TO_EMAILS else '---'}")
    print(f"Cc: {', '.join(CC_EMAILS) if CC_EMAILS else '---'}")
    print(f"Bcc: (hidden)")
    print(f"Subject: {subject}")
    print(f"Format: {'HTML' if send_html else 'Plain Text'}")
    print("\nBody:\n--------------------------------------")
    print(body[:500] + ("..." if len(body) > 500 else ""))
    print("--------------------------------------")
    print(f"Attachments: {', '.join(attachments) if attachments else 'None'}")
    print("====================================================\n")

    confirm = input("Send this email? (y/n): ").strip().lower()
    if confirm != "y":
        print("❌ Email cancelled.")
        return

    # ---------- Build Email ----------
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = ", ".join(TO_EMAILS)
    if CC_EMAILS:
        msg["Cc"] = ", ".join(CC_EMAILS)
    msg["Subject"] = subject

    if send_html:
        msg.attach(MIMEText(body, "html"))
    else:
        msg.attach(MIMEText(body, "plain"))

    for file in attachments:
        if os.path.exists(file):
            with open(file, "rb") as f:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(file)}")
            msg.attach(part)
            print(f"📎 Attached: {file}")
        else:
            print(f"⚠️ File not found, skipped: {file}")

    # ---------- Send Email ----------
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.sendmail(SENDER_EMAIL, all_recipients, msg.as_string())
        print("\n✅ Email sent successfully!")

        # ---------- Logging ----------
        email_id = str(uuid.uuid4())
        with open(LOG_FILE, "a", encoding="utf-8") as log:
            log.write("\n=============================\n")
            log.write(f"Email ID: {email_id}\n")
            log.write(f"Timestamp: {datetime.datetime.now()}\n")
            log.write(f"From: {SENDER_EMAIL}\n")
            log.write(f"To: {', '.join(TO_EMAILS) if TO_EMAILS else '---'}\n")
            log.write(f"Cc: {', '.join(CC_EMAILS) if CC_EMAILS else '---'}\n")
            log.write(f"Bcc: {', '.join(BCC_EMAILS) if BCC_EMAILS else '---'}\n")
            log.write(f"Subject: {subject}\n")
            log.write(f"Attachments: {', '.join(attachments) if attachments else 'None'}\n")
            log.write("=============================\n")

        print(f"📝 Email logged with ID: {email_id}")

    except Exception as e:
        print("\n❌ Failed to send email:", e)


def search_logs():
    """Search email logs by Email ID, Subject, or Date."""
    if not os.path.exists(LOG_FILE):
        print("⚠️ No log file found.")
        return

    print("\n=== SEARCH MENU ===")
    print("1. Search by Email ID")
    print("2. Search by Subject")
    print("3. Search by Date (YYYY-MM-DD)")
    choice = input("Choose an option (1-3): ").strip()

    search_term = input("Enter search term: ").strip().lower()
    found = False

    with open(LOG_FILE, "r", encoding="utf-8") as log:
        entry = []
        for line in log:
            if line.strip() == "=============================":
                if entry:
                    if choice == "1":  # Search by Email ID
                        if any(search_term in l.lower() for l in entry if l.lower().startswith("email id:")):
                            print("\n".join(entry))
                            print("=============================")
                            found = True
                    elif choice == "2":  # Search by Subject
                        if any(search_term in l.lower() for l in entry if l.lower().startswith("subject:")):
                            print("\n".join(entry))
                            print("=============================")
                            found = True
                    elif choice == "3":  # Search by Date
                        if any(search_term in l.lower() for l in entry if l.lower().startswith("timestamp:")):
                            print("\n".join(entry))
                            print("=============================")
                            found = True
                    entry = []
            entry.append(line.strip())

    if not found:
        print(f"❌ No emails found matching: {search_term}")


def main():
    """Main CLI loop."""
    while True:
        print("\n=== EMAIL SYSTEM ===")
        print("1. Send a new email")
        print("2. Search logs")
        print("3. Exit")

        choice = input("Choose an option (1-3): ").strip()

        if choice == "1":
            send_email()
        elif choice == "2":
            search_logs()
        elif choice == "3":
            print("👋 Goodbye!")
            break
        else:
            print("⚠️ Invalid option, try again.")


if __name__ == "__main__":
    main()
