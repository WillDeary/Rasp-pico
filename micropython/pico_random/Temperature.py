import machine
import utime

sensor_temp = machine.ADC(machine.ADC.CORE_TEMP)
led = machine.Pin(15, machine.Pin.OUT)
conversion_factor = 3.3 /(65535)
file = open("temps.txt", "w")

while True:
    led.value(1)
    utime.sleep(1)
    led.value(0)
    reading = sensor_temp.read_u16() * conversion_factor
    temp = 27- (reading -0.706)/0.001721
    file.write(str(temp) + "\n")
    file.flush()
    utime.sleep(10)