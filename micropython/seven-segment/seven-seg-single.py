from machine import Pin
import utime


pins = [
    Pin(4, Pin.OUT), # middle
    Pin(6, Pin.OUT), # top l
    Pin(0, Pin.OUT), # top
    Pin(3, Pin.OUT), # top r
    Pin(1, Pin.OUT), # b r
    Pin(7, Pin.OUT), # b 
    Pin(2, Pin.OUT), # bl
    Pin(5, Pin.OUT) # dp
]

def clear():
    for i in pins:
        i.value(1)
clear()
def on():
    for i in pins:
        i.value(0)

nums = [0x81,#0
        0xe7,#1
        0x49,#2
        0x43,#3
        0x27,#4
        0x13,#5
        0x11,#6
        0xc7,#7
        0x01,#8
        0x03,#9
        0x05,#A
        0x31,#B
        0x99,#C
        0x61,#D
        0x19,#E
        0x1d #F
        ]
while True:
    for i in range(len(nums)):
        a = [int(d) for d in str(bin(nums[i]))[2:]]
        if (len(a) <=7):
            zeros = 8 - len(a)
            for i in range(zeros):
                a.insert(0,0)
        print(a)
        for j in range(len(pins)):
              pins[j].value(a[j])
        utime.sleep(0.4)

  



        
    
