from uthingsboard.client import TBDeviceMqttClient
import json
from machine import Pin
import asyncio

from utils.wifi import WIFI
from utils.thingsboard import Thingsboard
from light_controller import LightController
from smart_light_controller import SmartLightController, Mode

wifi = WIFI()
thingsboard = Thingsboard()
light = LightController(thingsboard)
smart_light = SmartLightController(thingsboard, mode = Mode.SMART)
    
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
    elif method == "onLightSwitchToggle":
        smart_light.onLightSwitchToggle(params.get("ON"))
        thingsboard.client.send_rpc_reply(request_id, json.dumps({}))
    elif method == "onPIRStateChange":
        smart_light.onPIRStateChange(params.get("ON"))
        thingsboard.client.send_rpc_reply(request_id, json.dumps({}))
        
async def main():
    wifi.connect()
    thingsboard.connect(on_rpc_request)
    await thingsboard.subscribe_to_rpc()

try: 
    asyncio.run(main())
except KeyboardInterrupt:
    thingsboard.client.disconnect()
