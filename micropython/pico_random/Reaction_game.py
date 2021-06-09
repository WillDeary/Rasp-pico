import machine
import utime
import urandom
pressed = False

led = machine.Pin(15, machine.Pin.OUT)
left_led = machine.Pin(13, machine.Pin.OUT)
right_led = machine.Pin(11, machine.Pin.OUT)
left_button = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_DOWN)
right_button = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_DOWN)
buzzer = machine.Pin(12, machine.Pin.OUT)
fastest_button = None
fastest_time = 0

def button_handler(pin):
    global pressed
    if not pressed:
        pressed=True
        global fastest_button
        fastest_button = pin
        global fastest_time 
        fastest_time = utime.ticks_diff(utime.ticks_ms(), timer_start)
        print("The fastest reaction time " + str(fastest_time) +
            " milliseconds!")
        
led.value(1)
utime.sleep(urandom.uniform(1, 10))
led.value(0)
timer_start = utime.ticks_ms()
left_button.irq(trigger=machine.Pin.IRQ_RISING, handler=button_handler)
right_button.irq(trigger=machine.Pin.IRQ_RISING, handler=button_handler)

def buzzer_beep(number):
    for i in range(number):
        buzzer.value(1)
        utime.sleep(0.2)
        buzzer.value(0)
        utime.sleep(0.2)
        
def  turn_off_led(led):
    led.value(0)
    
def turn_on_led(led):
    led.value(1)
    
def flash_led(led):
    for i in range(20):
        turn_on_led(led)
        utime.sleep(0.1)
        turn_off_led(led)
        utime.sleep(0.1)
    
    
    
def winner(text, led):
    print(text)
    flash_led(led)
    
while fastest_button is None:
    utime.sleep(1)
    buzzer_beep(5)
if fastest_button is left_button:
    winner('Left Wins!',left_led )
elif fastest_button is right_button:
    winner('Right Wins!',right_led )
