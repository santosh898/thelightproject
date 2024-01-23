from machine import Pin

class LightController:

    led_pin = 5 
    light = Pin(led_pin, Pin.OUT)
    
    def turn_on(self):
        self.light.value(1)
        self.thingsboard.send_telemetry('ON', self.is_lit())

    def turn_off(self):
        self.light.value(0)
        self.thingsboard.send_telemetry('ON', self.is_lit())

    def set_status(self, status):
        if bool(status):
            self.turn_on()
        else:
            self.turn_off()

    def toggle(self):
        if self.is_lit():
            self.turn_off()
        else:
            self.turn_on()
        thingsboard.send_telemetry('ON', value)
        return self.is_lit()

    def is_lit(self):
        return bool(self.light.value())

    def __init__(self, thingsboard):
        self.thingsboard = thingsboard
