from machine import PWM
from time import sleep
import asyncio


class SmootherGauge:
    def __init__(self, pin, max_duty = 65535, update_interval=0.01, max_update_step=0.001, expected_value_update_interval=1):
        self.max_duty = max_duty
        self.pwm = PWM(pin)
        self.pwm.freq(10_000)
        self.pwm.duty_u16(0)
        
        self.current_value=0
        self.target_value=0
        self.update_step=0
        self.update_interval=update_interval
        self.max_update_step=max_update_step
        self.expected_value_update_interval=expected_value_update_interval
        

        
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
        self._update_update_step()
        
    def _update_update_step(self):
        diff = abs(self.current_value - self.target_value)
        self.update_step = diff / (self.expected_value_update_interval / self.update_interval)
        self.update_step = min(self.update_step,  self.max_update_step)
