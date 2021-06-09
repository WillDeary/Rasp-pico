import time
import picokeypad as keypad
import urandom
import math
keypad.init()
keypad.set_brightness(1.0)

lit = 0
last_button_states = 0
colour_index = 0

# returns 16
NUM_PADS = keypad.get_num_pads()

# turn lights off
for i in range(0, NUM_PADS):
    keypad.illuminate(i, 0x05, 0x05, 0x05)
    
keypad.update()

while True:
    # light between 1 and 3 lights
    random_lights = math.floor(urandom.uniform(1,6))
    # currently lit lights
    lit = []
    for i in range (0,random_lights):
        # choose rand btn to light
        random_btn = math.floor(urandom.uniform(0,NUM_PADS))
        # get random colors between 0x00 and 0x20
        random_colorR = urandom.getrandbits(6)
        random_colorG = urandom.getrandbits(6)
        random_colorB = urandom.getrandbits(6)
        keypad.illuminate(random_btn, random_colorR, random_colorG, random_colorB)
        keypad.update()
        lit.append(random_btn)
    time.sleep(0.5)
    for i in lit:
        keypad.illuminate(i, 0x05, 0x05, 0x05)
    keypad.update()

