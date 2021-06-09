import machine
import utime

sensor_pir = machine.Pin(28, machine.Pin.IN, machine.Pin.PULL_UP)
led = machine.Pin(15, machine.Pin.OUT)
buzzer = machine.Pin(14, machine.Pin.OUT)
def pir_handler(pin):
    utime.sleep_ms(100)
    if pin.value():
        print(sensor_pir.value())
        print("ALARM! Motion detected!")
        for i in range(50):
            led.toggle()
            buzzer.toggle()
            utime.sleep_ms(100)

sensor_pir.irq(trigger=machine.Pin.IRQ_RISING, handler=pir_handler)

while True:
    print(sensor_pir.value())
    led.toggle()
    utime.sleep(5)