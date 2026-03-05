import cv2
import pygame
import tkinter as tk
import time
import os

# --- CONFIGURATION ---
STOP_TEXT = "STOP_ALARM" 
EXT_CAM_INDEX = 0   # External USB Cam (Detection + Scan)
MAC_CAM_INDEX = 1   # Built-in Mac Cam (Scan Only)
ALARM_FILE = "alarm.mp3"

# Load detectors - Using absolute paths to prevent "File Not Found" errors
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
qr_detector = cv2.QRCodeDetector()

class UltimateInstantAlarm:
    def __init__(self, window):
        self.window = window
        self.window.title("Instant AI Alarm")
        self.active = False
        
        # 1. Initialize Sound
        pygame.mixer.init()
        if not os.path.exists(ALARM_FILE):
            print(f"ERROR: {ALARM_FILE} not found in this folder!")
        
        # 2. Open both cameras
        self.cap_ext = cv2.VideoCapture(EXT_CAM_INDEX)
        self.cap_mac = cv2.VideoCapture(MAC_CAM_INDEX)
        
        # Set resolution lower to speed up processing (prevents lag)
        self.cap_ext.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap_ext.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.label = tk.Label(window, text="STATUS: ARMED & WATCHING 👁️", font=("Arial", 16), fg="green")
        self.label.pack(pady=40)
        
        # Start the loop
        self.update_loop()

    def update_loop(self):
        ret_ext, frame_ext = self.cap_ext.read()
        ret_mac, frame_mac = self.cap_mac.read()
        
        if ret_ext and ret_mac:
            # --- PHASE 1: WATCHING (Detection) ---
            if not self.active:
                # Lighting Fix: Gray -> Equalize
                gray = cv2.cvtColor(frame_ext, cv2.COLOR_BGR2GRAY)
                gray = cv2.equalizeHist(gray) 
                
                # Detection Settings: 1.3 scale, 9 neighbors for balance
                faces = face_cascade.detectMultiScale(gray, 1.3, 9)
                
                if len(faces) > 0:
                    self.start_alarm()

            # --- PHASE 2: RINGING (QR Scanning) ---
            else:
                # Scan both cameras so you can use either one to stop it
                data_ext, _, _ = qr_detector.detectAndDecode(frame_ext)
                data_mac, _, _ = qr_detector.detectAndDecode(frame_mac)
                
                if data_ext == STOP_TEXT or data_mac == STOP_TEXT:
                    self.stop_alarm()

            # --- DISPLAY WINDOWS ---
            cv2.imshow("External Camera (Detector)", frame_ext)
            cv2.imshow("MacBook Camera (QR Scan)", frame_mac)
            
            # Use 'q' to emergency close
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.stop_all()
                return

        # Loop every 20ms (smooth performance)
        self.window.after(20, self.update_loop)

    def start_alarm(self):
        if not self.active:
            self.active = True
            self.label.config(text="PERSON DETECTED! SCAN QR!", fg="red")
            try:
                pygame.mixer.music.load(ALARM_FILE)
                pygame.mixer.music.play(-1) # Loop forever
            except Exception as e:
                print(f"Sound Error: {e}")

    def stop_alarm(self):
        if self.active:
            self.active = False
            pygame.mixer.music.stop()
            self.label.config(text="STATUS: ARMED & WATCHING 👁️", fg="green")

    def stop_all(self):
        # Cleanup to prevent webcam being "stuck" on
        self.cap_ext.release()
        self.cap_mac.release()
        cv2.destroyAllWindows()
        self.window.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x150")
    
    # Handle the "X" button on the window properly
    app = UltimateInstantAlarm(root)
    root.protocol("WM_DELETE_WINDOW", app.stop_all)
    
    root.mainloop()
