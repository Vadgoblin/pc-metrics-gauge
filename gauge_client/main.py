from machine import Pin, PWM
from time import sleep
import network
import requests
import time
import wifi
import config

from gauge import SimpleGauge
from metrics_collector import sync_http_get_metrics_collector

g1 = SimpleGauge(Pin(14), config.DUTY_CYCLE_4_GAUGE_100_PERCENT)
g2 = SimpleGauge(Pin(15), config.DUTY_CYCLE_4_GAUGE_100_PERCENT)

#for stats in sync_http_get_metrics_collector.iter_metrics(config.GET_ENDPOINT,3):
#    print(stats)

while True:
    try:
        #a = time.ticks_ms()
        #response = requests.get(config.ENDPOINT)
        #b = time.ticks_ms()
        #diffs = time.ticks_diff(b, a)
        #print(f"{diffs-(1000 * config.INTERVAL)} ms to get data")
        
        #if response.status_code != 200:
         #   print(response.content)
            
        #stats = response.json()
        stats = sync_http_get_metrics_collector.get_metrics(config.GET_ENDPOINT,3)
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
        g1.set_value(0)
        g2.set_value(0)
        sleep(config.INTERVAL)