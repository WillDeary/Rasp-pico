from machine import Pin
import utime as time
from dht import DHT11, InvalidChecksum, InvalidPulseCount
# Pico Explorer boilerplate
import picoexplorer as display

width = display.get_width()
height = display.get_height()
display_buffer = bytearray(width * height * 2)
display.init(display_buffer)


background = display.create_pen(28, 176, 250)  # Set pen to a converted HSV value
display.set_pen(background)  # Set pen to a converted HSV value
display.clear()           # Fill the screen with the colour
display.update()
i = 0

while True:
    try:
        # this if statement clears the display once the graph reaches the right hand side of the display
        if i >= (width + 1):
            i = 0
            display.set_pen(background)
            display.clear()
        
        time.sleep(1)
        pin = Pin(0, Pin.OUT, Pin.PULL_DOWN)
        sensor = DHT11(pin)
        t  = (sensor.temperature)
        h = (sensor.humidity)
        print("Temperature: {}".format(sensor.temperature))
        print("Humidity: {}".format(sensor.humidity))
        
        # draws a white background for the text
        display.set_pen(background)
        display.rectangle(0, 0, width, height-(height-92))

        # writes the reading as text in the white rectangle
        display.set_pen(0, 0, 0)
        
        # Clear the oled display in case it has junk on it
        display.set_pen(252, 245, 150)  # Set pen to color
        display.text("Temp: " + str(t) + "c", 25, 20, 240, 4)  # Add some text
        display.text("Humi: " + str(h) + "%", 25, 60, 240, 4)  # Add some text
        
        # chooses a pen colour based on the temperature
        display.set_pen(0, 255, 0)
        if t > 25:
            display.set_pen(255, 0, 0)
        if t < 13:
            display.set_pen(0, 0, 255)
            
        # draws the reading as a tall, thin rectangle
        display.rectangle(i, height - (int(t) * 4), 6, height)
        display.update()
        i +=6
        time.sleep(10)
    except InvalidPulseCount as e:
        print(e)
        time.sleep(10)
        continue
    
    