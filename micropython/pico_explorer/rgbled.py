from machine import Pin, PWM
import utime
 
red = Pin(0, Pin.OUT)
green = Pin(1, Pin.OUT)
blue = Pin(2, Pin.OUT)

red.value(0)
blue.value(0)
green.value(0)
while True:
    red.value(0)
    green.value(0)
    blue.value(0)
    utime.sleep(1)
 
    red.value(0)
    green.value(1)
    blue.value(1)
    utime.sleep(1)
 
    red.value(1)
    green.value(0)
    blue.value(1)    
    utime.sleep(1)
 
    red.value(1)
    green.value(1)
    blue.value(0)
    utime.sleep(1)
    
    red.value(0)
    green.value(1)
    blue.value(0)
    utime.sleep(1)