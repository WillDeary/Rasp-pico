import machine
import utime
potmeter = machine.ADC(26)
led = machine.PWM(machine.Pin(15))
led.freq(1000)
conversion_factor = 3.3 /(65535)
while True:
    led.duty_u16(potmeter.read_u16())