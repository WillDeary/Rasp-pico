# Physical Computing with Graphics on Pico Explorer
# 10K Ohm potentiometers on ADC pins
# LED with protection resistor approx 470 Ohms on GP4
# Tony Goodhew 4th March 2021 (Tested on Vers: 0.0.8)
import picoexplorer as display
import utime
import machine
width = display.get_width()
height = display.get_height()
display_buffer = bytearray(width * height * 2)
display.init(display_buffer)


def blk():
    display.set_pen(0,0,0)
    display.clear()
    display.update()

def vert(l,t,b):   # left, top, bottom
    n = b-t+1      # Vertical line
    for i in range(n):
        display.pixel(l, t+i)

def align(n, max_chars):
    # Aligns string of n in max_chars
    msg1 = str(n)
    space = max_chars - len(msg1)
    msg2 = ""
    for m in range(space):
        msg2 = msg2 +" "
    msg2 = msg2 + msg1
    return msg2  # String - ready for display
        
def showgraph(s,v,drop,rf,gf,bf):   # Bar graph
    display.set_pen(rf,gf,bf)
    display.text(s, 8, 8+drop, 240, 3)
    display.set_pen(0,0,0)        # Blank old bar graph
    display.rectangle(29, 10+drop, 240, 20)
    display.set_pen(rf,gf,bf)     # New  bar graph
    if v == 1:vert(29, 10+drop, 25) # Ensure these show up
    if v == 2:vert(30, 10+drop, 25)
    display.rectangle(29, 10+drop, v, 15)
    display.set_pen(100,100,100)  # Base line zero
    vert(28, 8+drop, 26+drop)             
    display.set_pen(200,200,200)
    # convert v to colour value (0 .. 255)
    num = int(v*2.55) 
    display.text(str(align(num,4)), 140, 9+drop, 240, 3)
    display.rectangle(210,9+drop,28,15)

# Mix colours
display.set_pen(200,200,200)
display.text("Adjust the pots", 40, 105, 230, 2)
display.text("Press Y button to halt", 5, 225, 230, 2)
running = True
while running:
    # Calculate percentages from pots
    rpot = int(display.get_adc(0) * 101)
    gpot = int(display.get_adc(1) * 101)
    bpot = int(display.get_adc(2) * 101)
    
    #Draw bar graphs using pertentages
    showgraph("R",rpot,0,255,0,0)
    showgraph("G",gpot,30,0,255,10)
    showgraph("B",bpot,60,0,0,255)
    # Calculate colour values from pots
    rv = int(display.get_adc(0) * 255)
    gv = int(display.get_adc(1) * 255)
    bv = int(display.get_adc(2) * 255)
    # Clear old RGB colours
    display.set_pen(0,0,0)
    display.rectangle(210,9,40,90)
    # Draw new RGB colours
    display.set_pen(rv,0,0)
    display.rectangle(210,9,20,15)
    display.set_pen(0,gv,0)
    display.rectangle(210,39,20,15)
    display.set_pen(0,0,bv)
    display.rectangle(210,69,20,15)
    #Draw mixed colour
    display.set_pen(rv,gv,bv)
    display.rectangle(20,130,200,80)
    # LED shows average brightness
    duty = int(250 * (rv+gv+bv)/3 -300)
    # Adjust for pot errors
    if duty < 0:
        duty = 0
    if duty > 65536:
        duty = 65500
    # led.duty_u16(duty)
    display.update()
    # Finished?
    if display.is_pressed(3): # Y button is pressed ?
        running = False
     

# Tidy up
blk()
#led.duty_u16(0)
display.set_pen(200,0,0)
display.text("All Done!", 55, 40, 200, 3)
display.update()
utime.sleep(2)
blk()
display.update()