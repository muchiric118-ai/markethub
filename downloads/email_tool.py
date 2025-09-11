import os
import smtplib
import zipfile
import json
import argparse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# ========================
# Email Sending Function
# ========================

def send_email(receiver_email, subject, body):
    from dotenv import load_dotenv
    load_dotenv()

    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("EMAIL_PASSWORD")

    if not sender_email or not sender_password:
        print("❌ Missing SENDER_EMAIL or EMAIL_PASSWORD in .env")
        return

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print(f"✅ Email sent to {receiver_email}")

        # Save log
        save_log(f"Email sent to {receiver_email} | Subject: {subject}")

    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        save_log(f"Failed to send email to {receiver_email} | Error: {e}")


# ========================
# Log Handling
# ========================

LOG_DIR = "logs"
ARCHIVE_DIR = "archives"
LOG_INDEX_FILE = "logs_index.json"

os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(ARCHIVE_DIR, exist_ok=True)

def save_log(message):
    """Save logs into daily files and zip them."""
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = os.path.join(LOG_DIR, f"{today}.log")

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} - {message}\n")

    # Archive daily logs
    archive_path = os.path.join(ARCHIVE_DIR, f"{today}.zip")
    with zipfile.ZipFile(archive_path, "a", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(log_file, os.path.basename(log_file))

    # Update index
    index = load_index()
    index[os.path.basename(log_file)] = archive_path
    with open(LOG_INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)


def load_index():
    if not os.path.exists(LOG_INDEX_FILE):
        return {}
    with open(LOG_INDEX_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def show_summary(zipf, fname, max_lines=5, show_all=False):
    if fname in zipf.namelist():
        with zipf.open(fname) as f:
            content = f.read().decode("utf-8", errors="ignore").splitlines()
            return content if show_all else content[:max_lines] + (["... (truncated)"] if len(content) > max_lines else [])
    return ["⚠️ File not found"]


def search_logs(query, extract=False, extract_dir="extracted_logs", search_content=False, summary=False, show_all=False, export=False):
    index = load_index()
    if not index:
        print("❌ No log index found.")
        return

    matches = {}
    for fname, archive in index.items():
        if not search_content and query.lower() in fname.lower():
            matches[fname] = archive
        elif search_content:
            with zipfile.ZipFile(archive, "r") as zipf:
                if fname in zipf.namelist():
                    with zipf.open(fname) as f:
                        try:
                            content = f.read().decode("utf-8", errors="ignore")
                            if query.lower() in content.lower():
                                matches[fname] = archive
                        except Exception:
                            pass

    if not matches:
        print(f"❌ No logs found for '{query}'.")
        return

    print(f"🔎 Found {len(matches)} matches for '{query}':")
    export_lines = []

    for fname, archive in matches.items():
        print(f"  - {fname} (in {archive})")
        with zipfile.ZipFile(archive, "r") as zipf:
            if summary or show_all:
                lines = show_summary(zipf, fname, show_all=show_all)
                print("📄 " + ("Full Log:" if show_all else "Preview:"))
                for line in lines:
                    print("   ", line)

                if export:
                    export_lines.append(f"===== {fname} ({archive}) =====")
                    export_lines.extend(lines)
                    export_lines.append("")

            if extract:
                os.makedirs(extract_dir, exist_ok=True)
                if fname in zipf.namelist():
                    zipf.extract(fname, extract_dir)
                    print(f"📂 Extracted to {os.path.join(extract_dir, fname)}")

    if export and export_lines:
        report_file = "search_results.txt"
        with open(report_file, "w", encoding="utf-8") as f:
            f.write("\n".join(export_lines))
        print(f"✅ Exported results to {report_file}")


# ========================
# CLI
# ========================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Email tool with log management")
    subparsers = parser.add_subparsers(dest="command")

    # ✅ Email sending command
    send_parser = subparsers.add_parser("send", help="Send email")
    send_parser.add_argument("--to", required=True, help="Recipient email")
    send_parser.add_argument("--subject", required=True, help="Email subject")
    send_parser.add_argument("--body", required=True, help="Email body")

    # ✅ Log search command
    log_parser = subparsers.add_parser("logs", help="Search and manage logs")
    log_parser.add_argument("--find", required=True, help="Search logs by filename or content")
    log_parser.add_argument("--extract", action="store_true", help="Extract found logs")
    log_parser.add_argument("--content", action="store_true", help="Search inside log contents")
    log_parser.add_argument("--summary", action="store_true", help="Show first 5 lines")
    log_parser.add_argument("--all", action="store_true", help="Show full log contents")
    log_parser.add_argument("--export", action="store_true", help="Export results to search_results.txt")

    args = parser.parse_args()

    if args.command == "send":
        send_email(args.to, args.subject, args.body)

    elif args.command == "logs":
        search_logs(
            args.find,
            extract=args.extract,
            search_content=args.content,
            summary=args.summary,
            show_all=args.all,
            export=args.export,
        )
