import time
import picokeypad as keypad
import urandom
import math
keypad.init()
keypad.set_brightness(1.0)

pressed_btn = 0
last_button_states = 0
colour_index = 0


# returns 16
NUM_PADS = keypad.get_num_pads()

def set_bit(x, n):
    return x | 1 << n

def wrong_btn_pressed():
    red_on = False
    for _ in range(11):                    
        for i in range(0,NUM_PADS):    
            if(red_on):                        
                keypad.illuminate(i, 0x20, 0x05, 0x05)
                keypad.update()                        
            else:                            
                keypad.illuminate(i, 0x05, 0x05, 0x05)
                keypad.update()
        time.sleep(0.3)                    
        red_on = not red_on

# turn lights low
for i in range(0, NUM_PADS):
    keypad.illuminate(i, 0x05, 0x05, 0x05)
    
keypad.update()
random_light_bit = 0x00

def random_c():
    return hex(math.floor(urandom.uniform(0,256)))

def wait_for_press(random_light_bit):
    pressed_btn = 0
    while (pressed_btn != random_light_bit):
        pressed_btn = 0
        button_states = keypad.get_button_states()
        if button_states > 0:
            button = 0
            for find in range(0, NUM_PADS):                                        
                # check if this button is pressed and no other buttons are pressed
                if button_states & 0x01 > 0:
                    if not (button_states & (~0x01)) > 0:
                        pressed_btn = pressed_btn | (1 << button)
                        time.sleep(0.1)
                        return pressed_btn
                    break
                button_states >>= 1
                button += 1         
            break    
    

memory_game_bits = []
memory_game_numbers = []

def turn_light_on(light, r,g,b):
    keypad.illuminate(light, r, g, b)
    keypad.update()
    
def turn_light_off(light):
    keypad.illuminate(light, 0x05, 0x05, 0x05)
    keypad.update()
    
while True:
    # illuminate random light from  0 - 15
    r = int(random_c())
    g = int(random_c())
    b = int(random_c())
    random_light_number = math.floor(urandom.uniform(0,15))
    memory_game_numbers.append(random_light_number)
    # the above number as the power of 2. ie convert to bit
    random_light_bit = set_bit(random_light_bit, random_light_number)
    memory_game_bits.append(random_light_bit)
    
    for light in memory_game_numbers:
         # Light the random light for debugging
        turn_light_on(light,r,g,b)
        time.sleep(1)
        turn_light_off(light)
        time.sleep(0.5)
        
            
    # get the pressed button and keep looking while one isn't pressed
    index = 0
    while(index < len(memory_game_bits)):
        light_bit = memory_game_bits[index]
        pressed_btn = 0    
        pressed_btn = wait_for_press(light_bit)
        
        # if the pressed button was correct then move on
        if(pressed_btn == light_bit):
            # correct button is pressed
            # repeat sequence and add new random light        
            print("WHOOO")
            time.sleep(0.2)
        # wrong button display red flashes    
        else:
            # wrong button is pressed flash red and reset game
            print("WASTE OF SPACE")
            wrong_btn_pressed()
            memory_game_bits = []
            memory_game_numbers = []
            break
        index = index + 1
    
    #keypad.illuminate(random_light_number, 0x05, 0x05, 0x05)
    #keypad.update()
    #time.sleep(0.4)
    pressed_btn = 0
    random_light_bit = 0x00
    wrongBtn = False
    