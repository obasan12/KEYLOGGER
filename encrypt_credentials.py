import json
from cryptography.fernet import Fernet

# Load the encryption key
with open("secret.key", "rb") as key_file:
    key = key_file.read()

cipher = Fernet(key)

# Replace with your actual email & app password
credentials = {
    "email": "gmail.com@gmail.com",
    "password": "gmail password"
}

# Encrypt credentials
encrypted_data = cipher.encrypt(json.dumps(credentials).encode())

# Save encrypted credentials to a file
with open("credentials.enc", "wb") as enc_file:
    enc_file.write(encrypted_data)

print("✅ Credentials encrypted and saved as 'credentials.enc'.")
