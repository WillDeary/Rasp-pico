import time
import picokeypad as keypad

keypad.init()
keypad.set_brightness(1.0)

while True:
    button_states = keypad.get_button_states()
    print(button_states)
    time.sleep(0.5)