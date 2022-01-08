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

led = machine.Pin(32, machine.Pin.OUT)
led_state = False
led.value(led_state)

def short_cb(led):
    led.value(not led.value())

button = ubutton(
        pin=machine.Pin(25, machine.Pin.IN),
        cb_short=short_cb,
        shrt_args=[led],
        irq=machine.Pin.IRQ_RISING,
    )

# ToDo: Add MQTT publish, dimmer callback
# timer_1 = Timer(1)
# # ToDo: Add photoresistor monitoring and condition to turn led on and off
# timer_1.init(period=2000, mode=Timer.PERIODIC, callback=lambda t:print(1))