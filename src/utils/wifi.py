import network
from time import sleep

class WIFI:

    def connect(self):
        ssid,password = self.get_credentials()
        print(ssid)
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
        # get from eeprom here
        ssid = "Internet Khomba"
        password = "iamfromjhasuguda"
        return ssid, password

if __name__ == "__main__":
    wifi = WIFI()
    wifi.connect()
