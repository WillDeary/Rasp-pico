from machine import Pin
from utime import sleep

data_p = Pin(0, Pin.OUT)
clock = Pin(1, Pin.OUT)
latch = Pin(2,Pin.OUT)
clear = Pin(3, Pin.OUT, Pin.PULL_UP)

digit_1 = Pin(4, Pin.OUT)
digit_2 = Pin(15, Pin.OUT)
digit_3 = Pin(13, Pin.OUT)
digit_4 = Pin(14, Pin.OUT)

digit_1.value(0)
digit_2.value(1)
digit_3.value(1)
digit_4.value(1)

digits = [digit_1, digit_2, digit_3, digit_4]

data_p.value(0)
clock.value(0)
latch.value(0)

off   = 0b00000000
num_0 = 0b11111100
num_1 = 0b01100000
num_2 = 0b11011010
num_3 = 0b11110010
num_4 = 0b01100110
num_5 = 0b10110110
num_6 = 0b10111110
num_7 = 0b11100000
num_8 = 0b11111110
num_9 = 0b11110110

numbers = [num_0, num_1, num_2, num_3, num_4, num_5, num_6, num_7, num_8, num_9, off]

def clear_f():
    clear.low()
    clear.high()

def tick_f():
    clock.low()
    clock.high()
    
def latch_f():
    latch.high()
    latch.low()
    
def write(value):
    clear_f()
    for i in range(8):
        data = value >> i & 1    
        if data == 0:
            data_p.high()
        else:
            data_p.low()
        tick_f()
    latch_f()


def digits_off():
    for digit in digits:
        digit.value(1)
       
def select_digit(digit):
    digits_off()
    if(digit == 1):
        digits[0].value(0)
    elif digit ==2:
        digits[1].value(0)
    elif digit ==3:
        digits[2].value(0)
    elif digit ==4:
        digits[3].value(0)
            
def display(num):
    write(off)
    select_digit(4)
    write(numbers[num%10])
    write(off)
    select_digit(3)
    write(numbers[num%100//10])
    write(off)
    select_digit(2)
    write(numbers[num%1000//100])
    write(off)
    select_digit(1)
    write(numbers[num%10000//1000])
    

for numb in range(10000, 0, -1):
    for i in range(50):
        display(numb)
    