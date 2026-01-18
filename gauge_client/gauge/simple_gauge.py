from machine import PWM

class SimpleGauge:
    def __init__(self, pin, max_duty = 65535):
        self.max_duty = max_duty
        self.pwm = PWM(pin)
        self.pwm.freq(10_000)
        self.pwm.duty_u16(0)
        
    def set_value(self, value):
        if value < 0 or value > 1:
            raise Exception("Value must be beetween 0 and 1.")
        self.pwm.duty_u16(int(value * self.max_duty))
