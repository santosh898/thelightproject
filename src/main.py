from uthingsboard.client import TBDeviceMqttClient
import network
import json
from time import sleep
from machine import Pin

# Configure your WiFi credentials
wifi_ssid = "ssid"
wifi_password = "password"

led_pin = 5  # Assuming this is the led pin

led = Pin(led_pin, Pin.OUT)

def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    
def get_led_status():
    return json.dumps({"ON":bool(led.value())})

def set_led_status(status):
    led.value(int(status))
    return get_led_status()
    
def on_rpc_request(client,request_id, method, params):
    print(f"Received RPC request - Method: {method}, Params: {params}")
    if method == "getLedStatus":
        client.send_rpc_reply(request_id,get_led_status())
        send_telemetry(client, led.value())
    elif method == "setLedStatus":
        client.send_rpc_reply(request_id,set_led_status(params.get("ON")))
        send_telemetry(client, led.value())
    
def connect_client():
    client = TBDeviceMqttClient('192.168.29.54', access_token='light-1')
    client.set_server_side_rpc_request_handler(lambda req_id, method, params: on_rpc_request(client, req_id, method, params))
    print("subscribed for rpc")
    client.connect()
    return client

def send_telemetry(client, value):
    telemetry = {'ON': value}
    client.send_telemetry(telemetry)
    
def subscribe_rpc(client):
    while True:
        client.wait_msg()
    

try:
    connect_to_wifi(wifi_ssid, wifi_password)
    client = connect_client()
    subscribe_rpc(client)
except KeyboardInterrupt:
    client.disconnect()
