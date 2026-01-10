from machine import Pin, PWM
from time import sleep
import network
import requests
import time
import wifi
import config

from gauge import SimpleGauge

g1 = SimpleGauge(Pin(14))
g2 = SimpleGauge(Pin(15))

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
        
        g1.set_value(cpu_usage / 100)
        g2.set_value(ram_usage / 100)
    except Exception as e:
        print(e)
        sleep(config.INTERVAL)