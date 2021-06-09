from machine import Pin, PWM
import utime
import urandom
import math
 
red = Pin(0, Pin.OUT)
green = Pin(1, Pin.OUT)
blue = Pin(2, Pin.OUT)
pwmred = PWM(red)
pwmgreen= PWM(green)
pwmblue= PWM(blue)
ledarr = [pwmred,pwmgreen,pwmblue]
for color in ledarr:
    color.freq(1000)
    color.duty_u16(0)
    print(color.duty_u16())
duty = 0
direction = 1

for _ in range(10000):
    rgb = math.floor(urandom.uniform(0,3 ))
    color = ledarr[rgb]
    duty += direction
    print(duty)
    if duty > 255:
        duty = 255
        direction = -1
        utime.sleep(1)
    elif duty < 0:
        duty = 0
        direction = 1
        utime.sleep(1)
    color.duty_u16(duty*duty)
    
    utime.sleep(0.01)
    