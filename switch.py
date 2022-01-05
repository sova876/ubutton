import machine
import time
import connect
# import uasyncio

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

counter = 5
led_state = False
led.value(led_state)

btn_tmr = 0
btn_flag = 0

while counter > 0:
    # ToDo: Add MQTT publish, ubutton class, uasyncio
    btn_state = button.value()
    if btn_state and not btn_flag and time.ticks_ms() - btn_tmr > 50:
        btn_flag = 1
        print("Pressed!")
        # ToDo: Add double press
        btn_tmr = time.ticks_ms()
    elif btn_state and btn_flag and time.ticks_ms() - btn_tmr > 200:
        print("Hold!")
        # ToDo: Add dimmer option
    elif not btn_state and btn_flag and time.ticks_ms() - btn_tmr > 1000:
        btn_flag = 0
        print("Long release!")
        counter -= 1
        led_state = False
    elif not btn_state and btn_flag and 50 < time.ticks_ms() - btn_tmr < 1000:
        btn_flag = 0
        print("Short release!")
        led_state = not led_state
    led.value(led_state)

print("Done!")
led.value(0)