from light_controller import LightController
import asyncio

class Mode:
    MANUAL = 0
    SMART = 1
    OVERRIDE = 2

class SmartLightController:
    
    def __init__(self, thingsboard, mode = Mode.MANUAL):
        self._mode = mode
        self.thingsboard = thingsboard
        self.light = LightController(thingsboard)
    
    @property
    def mode(self):
        return self._mode
    
    @mode.setter
    def mode(self, value):
        if value in (Mode.MANUAL, Mode.SMART, Mode.OVERRIDE):
            self._mode = value
            self.thingsboard.send_telemetry("MODE", self.mode)
        else:
            raise ValueError(f"Invalid mode: {value}. Choose from 0 or 1 or 2")
        
    async def runAfter(self,delay,callback):
        await asyncio.sleep(delay)
        callback()
        
    def turnLightOff(self):
        self.light.turn_off()
        
    async def smartModeT(self):
        await asyncio.sleep(3)
        self.turnLightOff()
        
    def onPIRStateChange(self, isOn):
        if self.mode == Mode.SMART:
            self.light.set_status(isOn)
            if isOn:
                self.smartModeTask = asyncio.create_task(self.runAfter(10,self.turnLightOff))
                # start smart mode timer
            else:
                self.smartModeTask.cancel()
                # disable smart mode timer
                
    def switchToSmartMode(self):
        self.mode = Mode.SMART
                
    def onLightSwitchToggle(self, isOn):
        self.light.set_status(isOn)
        if self.mode == Mode.OVERRIDE:
            self.overrideModeTask.cancel()
        self.mode = Mode.OVERRIDE
        self.overrideModeTask = asyncio.create_task(self.runAfter(10,self.switchToSmartMode))
        # start override mode timer
