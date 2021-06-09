from machine import ADC, Pin
import time
adc1 = ADC(26)
adc2 = ADC(27)
adc3 = ADC(28)

while True:
    print("ADC1" + str(adc1.read_u16()))
    print("ADC2" + str(adc2.read_u16()))
    print("ADC3" + str(adc3.read_u16()))
    time.sleep(1)