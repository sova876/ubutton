import machine
import ubinascii
from mqtt import MQTTClient
import json

def wifi_connect(ssid, password):
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())

def mqtt_conected_callback(connected):
    global mqtt_client
    if connected:
        mqtt_client.publish('esp32/connected', str(1))
        print('subscribtion ...')
        mqtt_client.subscribe('hass/esp32/button_25')
        mqtt_client.subscribe('hass/esp32/button_26')
        print('subscribtion ok')

with open("wlanconfig.json","r") as handler:
    info = json.load(handler)

ssid = info["ssid"]
password = info["wlanpassword"]
mqtt_server = info["mqtt_server"]
mqtt_user = info["mqtt_user"]
mqtt_pass = info["mqtt_pass"]

client_id = ubinascii.hexlify(machine.unique_id())

mqtt_client = MQTTClient(mqtt_server, port=1883)
mqtt_client.set_connected_callback(mqtt_conected_callback)

wifi_connect(ssid, password)
mqtt_client.connect(client_id, user=mqtt_user, password=mqtt_pass)