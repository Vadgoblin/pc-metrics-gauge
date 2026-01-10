from machine import Pin, PWM
from time import sleep
import network
import requests
import time

import wifi
import config


pwm1 = PWM(Pin(14))
pwm1.freq(10_000)

pwm2 = PWM(Pin(15))
pwm2.freq(10_000)

pwm1.duty_u16(0)
pwm2.duty_u16(0)


while True:
    try:
        a = time.ticks_ms()
        response = requests.get(config.ENDPOINT)
        b = time.ticks_ms()
        diffs = time.ticks_diff(b, a)
        print(diffs-(1000 * config.INTERVAL))
        
        if response.status_code != 200:
            print(response.content)
            
        stats = response.json()
        print(stats)
        cpu_temp = stats['cpu_temp']
        cpu_usage = stats['cpu_usage']
        ram_usage = stats['ram_usage']
        
        cpu_temp = max(0,min(100, cpu_temp))
        cpu_usage = max(0,min(100, cpu_usage))
        ram_usage = max(0,min(100, ram_usage))
        
        pwm1.duty_u16(int(cpu_usage * config.DUTY_CYCLE_4_GAUGE_100_PERCENT / 100))
        pwm2.duty_u16(int(cpu_temp * config.DUTY_CYCLE_4_GAUGE_100_PERCENT / 100))
    except:  
        sleep(config.INTERVAL)