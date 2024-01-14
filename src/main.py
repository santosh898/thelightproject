from uthingsboard.client import TBDeviceMqttClient
import json
from machine import Pin

from utils.wifi import WIFI
from utils.thingsboard import Thingsboard

from light_controller import LightController

led_pin = 5  # Assuming this is the led pin

led = Pin(led_pin, Pin.OUT)

wifi = WIFI()
thingsboard = Thingsboard()
light = LightController(thingsboard)
    
def get_light_status():
    return json.dumps({"ON": light.is_lit() })

def set_light_status(status):
    light.set_status(status)
    return get_light_status()
    
def on_rpc_request(request_id, method, params):
    print(f"Received RPC request - Method: {method}, Params: {params}")
    if method == "getLightStatus":
        thingsboard.client.send_rpc_reply(request_id, get_light_status())
    elif method == "setLightStatus":
        thingsboard.client.send_rpc_reply(request_id, set_light_status(params.get("ON")))

try:
    wifi.connect()
    thingsboard.connect(on_rpc_request)
    thingsboard.subscribe_to_rpc()
except KeyboardInterrupt:
    thingsboard.client.disconnect()
