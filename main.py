import machine
from ubutton import ubutton
import time

# Example for ESP32.
# ESP32 pins are outputs and initially set to 0.
led_idxs = [32,25,27]
leds = {led : machine.Pin(led, machine.Pin.OUT) for led in led_idxs}
[leds[led].value(0) for led in led_idxs] #All pins' outputs are set to 0

#Simple example function for callbacks.
def toggle(led):
    #A toggle callback
    led.value(not led.value())

def master(leds):
    #A master switch
    for led in leds:
        led.value(0)

#Set callbacks dict. 
#1,2,3: callbacks for 1-click, 2-clicks, and 3-clicks respectively. 
#'long' is for a callback after long press.
callbacks = {1: toggle, 2: toggle, 3: toggle, 'long': master}
cb_args = {1: [leds[32]], 2: [leds[25]], 3: [leds[27]], 'long': [list(leds.values())]}
callback_kwargs = {'cbs': callbacks, 'cb_args': cb_args}

button14 = ubutton(
        pin=machine.Pin(14, machine.Pin.IN),
        irq=machine.Pin.IRQ_RISING,
        bounce_time=50, long_time=500, click_timeout = 500, downtime = 2000, 
        **callback_kwargs
    )