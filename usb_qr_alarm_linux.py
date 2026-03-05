import cv2
import pygame
import tkinter as tk
import os

# --- CONFIGURATION ---
STOP_TEXT = "STOP_ALARM" 
EXT_CAM_INDEX = 2   # Your /dev/video2 (USB)
MAC_CAM_INDEX = 0   # Your /dev/video0 (Laptop)
ALARM_FILE = "alarm.mp3"

# Load detectors
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
qr_detector = cv2.QRCodeDetector()

class LinuxInstantAlarm:
    def __init__(self, window):
        self.window = window
        self.window.title("Linux AI Alarm")
        self.active = False
        
        # 1. Initialize Sound
        pygame.mixer.init()
        if not os.path.exists(ALARM_FILE):
            print(f"CRITICAL: {ALARM_FILE} not found!")

        # 2. Open cameras with Linux-specific V4L2 backend
        self.cap_ext = cv2.VideoCapture(EXT_CAM_INDEX, cv2.CAP_V4L2)
        self.cap_mac = cv2.VideoCapture(MAC_CAM_INDEX, cv2.CAP_V4L2)
        
        # 3. Force MJPEG for speed on Linux
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        for cap in [self.cap_ext, self.cap_mac]:
            cap.set(cv2.CAP_PROP_FOURCC, fourcc)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.label = tk.Label(window, text="STATUS: WATCHING (LINUX) 👁️", font=("Arial", 16), fg="green")
        self.label.pack(pady=40)
        self.update_loop()

    def update_loop(self):
        ret_ext, frame_ext = self.cap_ext.read()
        ret_mac, frame_mac = self.cap_mac.read()
        
        if ret_ext and ret_mac:
            if not self.active:
                # Detection on External Cam
                gray = cv2.cvtColor(frame_ext, cv2.COLOR_BGR2GRAY)
                gray = cv2.equalizeHist(gray) # Lighting fix
                faces = face_cascade.detectMultiScale(gray, 1.3, 7)
                if len(faces) > 0:
                    self.start_alarm()
            else:
                # QR Scanning on both
                data_ext, _, _ = qr_detector.detectAndDecode(frame_ext)
                data_mac, _, _ = qr_detector.detectAndDecode(frame_mac)
                if data_ext == STOP_TEXT or data_mac == STOP_TEXT:
                    self.stop_alarm()

            cv2.imshow("External (Detector)", frame_ext)
            cv2.imshow("Laptop (QR Scan)", frame_mac)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.stop_all()
                return

        self.window.after(10, self.update_loop)

    def start_alarm(self):
        if not self.active:
            self.active = True
            self.label.config(text="PERSON DETECTED!", fg="red")
            try:
                pygame.mixer.music.load(ALARM_FILE)
                pygame.mixer.music.play(-1)
            except: pass

    def stop_alarm(self):
        self.active = False
        pygame.mixer.music.stop()
        self.label.config(text="STATUS: WATCHING (LINUX) 👁️", fg="green")

    def stop_all(self):
        self.cap_ext.release()
        self.cap_mac.release()
        cv2.destroyAllWindows()
        self.window.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x150")
    app = LinuxInstantAlarm(root)
    root.mainloop()
