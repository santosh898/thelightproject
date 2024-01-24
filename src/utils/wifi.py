import network
from time import sleep
from mpy_env import get_env

class WIFI:

    def connect(self):
        ssid,password = self.get_credentials()
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(ssid, password)
        print("connecting")
        while wlan.isconnected() == False:
            print('Waiting for connection...')
            sleep(1)
        ip = wlan.ifconfig()[0]
        print(f'Connected on {ip}')

    def get_credentials(self):
        config = get_env("wifi")
        return config.get("ssid"), config.get("password")

if __name__ == "__main__":
    wifi = WIFI()
    wifi.connect()
