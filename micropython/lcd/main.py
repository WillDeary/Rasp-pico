import time
import board
import busio
from pico_i2c_lcd_cypi import I2cLcd

# Modify this if you have a different sized Character LCD
lcd_columns = 16
lcd_rows = 2

# Initialise I2C bus.
i2c = busio.I2C(scl=board.GP3, sda=board.GP2)

# Initialise the lcd class
lcd = I2cLcd(i2c, 0x27, lcd_rows, lcd_columns)

lcd.move_to(0,0)
lcd.putstr('I Love Kristin!')
