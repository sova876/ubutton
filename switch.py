import machine
import time
import connect
from machine import Timer

def message_callback(topic, payload):
    global led_state
    print('topic: {}, msg: {}'.format(topic, payload))
    if int(topic.decode('utf-8')[-2:]) is 25:
        led_state = not led_state
        led.value(led_state)

led = machine.Pin(32, machine.Pin.OUT)
button = machine.Pin(25, machine.Pin.IN)

# connect.mqtt_client.subscribe('hass/esp32/button_25')
connect.mqtt_client.set_message_callback(message_callback)

led_state = False
led.value(led_state)

def cb_handler(pin):

    global led_state, led

    handled = False
    btn_tmr = 0
    btn_flag = 0

    while not handled:
        btn_state = pin.value()
        if btn_state and not btn_flag and time.ticks_ms() - btn_tmr > 50:
            btn_flag = 1
            print("Pressed!")
            # ToDo: Add double click detection
            btn_tmr = time.ticks_ms()
        elif btn_state and btn_flag and time.ticks_ms() - btn_tmr > 200:
            print("Hold!")
            # ToDo: Add dimmer option
        elif not btn_state and btn_flag and time.ticks_ms() - btn_tmr > 1000:
            btn_flag = 0
            print("Long release!")
            led_state = False
            handled = True
        elif not btn_state and btn_flag and 50 < time.ticks_ms() - btn_tmr < 1000:
            btn_flag = 0
            print("Short release!")
            led_state = not led_state
            handled = True
        led.value(led_state)

# ToDo: Add MQTT publish, ubutton class
button.irq(handler=cb_handler, trigger=machine.Pin.IRQ_RISING)

timer_1 = Timer(1)
# ToDo: Add photoresistor monitoring and condition to turn led on and off
timer_1.init(period=1000, mode=Timer.PERIODIC, callback=lambda t:print(1))