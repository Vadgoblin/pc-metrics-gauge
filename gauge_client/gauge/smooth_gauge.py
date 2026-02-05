from machine import PWM
from time import sleep
import asyncio


class SmoothGauge:
    def __init__(self, pin, max_duty = 65535, update_interval=0.01, update_step=0.001):
        self.max_duty = max_duty
        self.pwm = PWM(pin)
        self.pwm.freq(10_000)
        self.pwm.duty_u16(0)
        
        self.current_value=0
        self.target_value=0
        self.update_interval=update_interval
        self.update_step=update_step
        

        
        asyncio.create_task(self._loop())
    
    async def _loop(self):
        while True:
            if self.current_value != self.target_value:
                diff = self.target_value - self.current_value
                diff = max(-self.update_step, min(self.update_step, diff))
                self.current_value += diff
                self.pwm.duty_u16(int(self.current_value * self.max_duty))
                
            await asyncio.sleep(self.update_interval)


    def set_value(self, value):
        if value < 0 or value > 1:
            raise Exception("Value must be beetween 0 and 1.")
        
        self.target_value = value