# Keylogger Project

## 📌 Project Overview
This project is a **Keylogger** built in **C++**, designed to capture keystrokes and store them in a log file. The logs are encrypted and can be sent via email after reaching a specified file size limit. This project includes additional features for stealth operation and security.

## 🚀 Features
- **Keylogging**: Captures and records keystrokes.
- **Log Encryption**: Uses AES encryption to secure log files.
- **Email Sending**: Automatically sends logs via email when file size limit is reached.
- **Stealth Mode**: Runs silently in the background.
- **Cross-Platform Support**: Works on Windows and (future) Linux versions.
- **Self-Destruct Feature**: Optionally deletes logs after sending.
- **Persistence**: Can be configured to start on boot.

## 🔧 Installation & Setup
### Prerequisites
- Windows OS
- MinGW Compiler for C++
- Python (for email sending script)
- Pyarmor (for obfuscation, if needed)

### Steps to Compile & Run
1. **Clone the Repository**:
   ```sh
   https://github.com/obasan12/KEYLOGGER.git
   cd keylogger_project
   ```
2. **Compile the Keylogger**:
   ```sh
   g++ keylogger.cpp -o keylogger.exe
   ```
3. **Run the Keylogger**:
   ```sh
   keylogger.exe
   ```
4. **Check Log File**:
   - The log file (`log.txt`) will be generated in the same directory as the executable.

## 📤 Email Configuration
To enable email log sending:
1. Open `config.json` and update your SMTP credentials.
2. Run `encrypt_credentials.py` to encrypt your credentials.
3. Ensure `send_email.py` is executed periodically.

## 🔒 Security & Ethical Disclaimer
This project is for **educational purposes only**. Unauthorized use of keyloggers is **illegal** and may violate privacy laws. Use this tool **only with explicit permission**.

## 📜 License
This project is licensed under the **MIT License**.

## 🤝 Contributing
Feel free to open **issues** or submit **pull requests** to improve this project.

## 📞 Contact
For any inquiries, contact **Emerickcipher@gmail.com** or open an issue on GitHub.

--
more coming
Appriciate 
