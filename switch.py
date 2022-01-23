import machine
from ubutton import ubutton
import time
# import connect
from machine import Timer

# def message_callback(topic, payload):
#     global led_state
#     print('topic: {}, msg: {}'.format(topic, payload))
#     if int(topic.decode('utf-8')[-2:]) is 25:
#         led_state = not led_state
#         led.value(led_state)

# connect.mqtt_client.subscribe('hass/esp32/button_25')
# connect.mqtt_client.set_message_callback(message_callback)

led_idxs = [32,25,27]
leds = {led : machine.Pin(led, machine.Pin.OUT) for led in led_idxs}
[leds[led].value(0) for led in led_idxs]

def toggle(led):
    led.value(not led.value())

def master(leds):
    for led in leds:
        led.value(0)

callbacks = {1: toggle, 2: toggle, 3: toggle}
cb_args = {1: [leds[32]], 2: [leds[25]], 3: [leds[27]]}
callback_args = {'cbs': callbacks, 'cb_args': cb_args}

button14 = ubutton(
        pin=machine.Pin(14, machine.Pin.IN),
        irq=machine.Pin.IRQ_RISING,
        bounce_time=50, long_time=500, click_timeout = 500, downtime = 2000, 
        **callback_args
    )
    
callbacks = {1: toggle, 'long': master}
cb_args = {1: [leds[25]], 'long': [list(leds.values())]}
callback_args = {'cbs': callbacks, 'cb_args': cb_args}

button12 = ubutton(
        pin=machine.Pin(12, machine.Pin.IN),
        irq=machine.Pin.IRQ_RISING,
        bounce_time=50, long_time=500, click_timeout = 500, downtime = 2000, 
        **callback_args
    )

def timer_cb(adc, pin):
    illumin_state = adc.read()
    if illumin_state > 3500:
        print("Dark!")
        # pin.value(1)

class usensor(object):

    def __init__(self, pin, sensor, poll_period):
        self.pin = pin
        self.sensor = sensor
        self.period = poll_period

        timer_1 = Timer(1)
        timer_1.init(period=self.period, mode=Timer.PERIODIC, callback=self.cb)

    def cb(self, timer_1):
        reading = self.sensor.read()
        print('Sensor readings: ', reading)
        if reading > 3500:
            self.pin.value(1)
        elif reading < 2000:
            self.pin.value(0)

adc = machine.ADC(machine.Pin(34))
# ToDo: Add MQTT publish, dimmer callback
# timer_1 = Timer(1)
# ToDo: Add photoresistor monitoring and condition to turn led on and off
# timer_1.init(period=2000, mode=Timer.PERIODIC, callback=timer_cb)
sensor = usensor(pin = leds[27], sensor = adc, poll_period=2000)