from uthingsboard.client import TBDeviceMqttClient
from time import sleep
import asyncio

class Thingsboard:

    client = None

    def connect(self,on_rpc_request):
        ip, access_token = self.get_credentials()
        self.client = TBDeviceMqttClient(ip, access_token=access_token)
        self.client.set_server_side_rpc_request_handler(on_rpc_request)
        print("subscribed for rpc")
        self.client.connect()

    def send_telemetry(self, key, value):
        self.client.send_telemetry({key:value})

    def subscribe_to_rpc(self):
        while True:
            await asyncio.sleep(1)
            self.client.check_msg()

    def get_credentials(self):
        # get from eeprom
        ip = '192.168.0.252'
        access_token = 'light-1'
        return ip, access_token
