# 🚨 AI QR Security Alarm

A dual-camera security system that triggers an alarm via **AI Person Detection** on an external USB webcam and only deactivates by scanning a **QR Code**.

## 🛠️ Setup

### 1. Requirements
*   **Python 3.9+**
*   **Webcams**: 1 Internal (MacBook/Linux PC), 1 External Webcam (USB).
*   **Libraries**: `opencv-python`, `pygame`, `tkinter`.

### 2. Installation

**On macOS:**
```bash
pip install opencv-python pygame

On linux:  sudo apt update
sudo apt install python3-opencv python3-pygame python3-tk v4l-utils -y

There is a default alarm sound but you can switch it with your own mp3 file.

For running on mac: python usb_qr_alarm.py  or python3 usb_qr_alarm.py
if the first one doesn't work.

For running on linux: python3 usb_qr_alarm_linux.py

For changing sensitivity, find detectMultiScale(gray, 1.1, 3) in the .py file and change the last number higher to lower sensitivity.

Scan QR: Show your code to either camera to stop the alarm.
Q Key: Press 'q' on any video window to Emergency Exit.
