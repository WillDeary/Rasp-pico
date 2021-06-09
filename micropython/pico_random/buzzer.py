from machine import Pin
from utime import sleep
buzzer = Pin(0, Pin.OUT)

while True:
    buzzer.toggle()
    sleep(0.5)
