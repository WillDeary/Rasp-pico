from rgbkeypad import RGBKeypad
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# map the position of the keys on the RGBKeypad to keyboard strokes
# circuitpython keycodes can be found here - 
#   https://github.com/adafruit/Adafruit_CircuitPython_HID/blob/master/adafruit_hid/keycode.py
KEYBOARD_MAP = {
    (0,0): (Keycode.SHIFT, Keycode.M,),
    (1,0): (Keycode.A,),
    (2,0): (Keycode.R,),
    (3,0): (Keycode.T,),
    (0,1): (Keycode.SHIFT, Keycode.W,),
    (1,1): (Keycode.O,),
    (2,1): (Keycode.Z,),
    (0,2): (Keycode.SHIFT, Keycode.E,),
    (1,2): (Keycode.R,),
    (2,2): (Keycode.E,),
    (3,2): (Keycode.SHIFT, Keycode.ONE,),
    (3,3): (Keycode.CONTROL, Keycode.SHIFT, Keycode.UP_ARROW),
}

# what colors to use if an assigned/unassigned key is pressed
VALID_KEY_COLOR = (0, 0, 255)
INVALID_KEY_COLOR = (255, 0, 0)

keypad = RGBKeypad()
kbd = Keyboard(usb_hid.devices)
keypad.clear()
while True:
    # loop through all the keys
    for key in keypad.keys:
        if (key.x, key.y) in KEYBOARD_MAP.keys():
            key.color = (0,0,255)
        else:
            key.color = (255,0,0)
        # has a key been pressed?
        if key.is_pressed():
            # does this key have a keyboard mapping
            if (key.x, key.y) in KEYBOARD_MAP.keys():            
                # debug - print out the keyboard strokes
                print(KEYBOARD_MAP[(key.x, key.y)])
                key.color = VALID_KEY_COLOR
                # send the keyboard strokes
                kbd.send(*KEYBOARD_MAP[(key.x, key.y)]) 
            else:
                key.color = INVALID_KEY_COLOR
            
            # what for the key to be released
            while key.is_pressed():
                pass
            key.clear()