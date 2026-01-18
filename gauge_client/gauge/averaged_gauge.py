from machine import PWM

class AveragedGauge:
    def __init__(self, pin, max_duty = 65535, history_size=25):
        self.max_duty = max_duty
        self.pwm = PWM(pin)
        self.pwm.freq(10_000)
        self.pwm.duty_u16(0)
        self.history_size = history_size
        self.history = []
        
    def set_value(self, value):
        if value < 0 or value > 1:
            raise Exception("Value must be beetween 0 and 1.")
        self.history.append(value)
        
        while len(self.history) > self.history_size:
            self.history.pop(0)
            
        avg_value = sum(self.history) / len(self.history)
        print(value)
        self.pwm.duty_u16(int(avg_value * self.max_duty))

