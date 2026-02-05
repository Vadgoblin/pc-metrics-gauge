import uasyncio as asyncio
from machine import Pin
from time import sleep
import wifi
import config

from metrics_collector import AsyncHttpGetMetricsCollector, AsyncWebsocketMetricsCollector
from gauge import SmoothGauge


# pinout of my board is kinda funky
# 3 2 0 4
g1 = SmoothGauge(Pin(3), config.DUTY_CYCLE_4_GAUGE_100_PERCENT)
g2 = SmoothGauge(Pin(2), config.DUTY_CYCLE_4_GAUGE_100_PERCENT)
g3 = SmoothGauge(Pin(0), config.DUTY_CYCLE_4_GAUGE_100_PERCENT)
g4 = SmoothGauge(Pin(4), config.DUTY_CYCLE_4_GAUGE_100_PERCENT)

wifi.connect(config.SSID, config.PASSWORD)

#metrics_collector = AsyncHttpGetMetricsCollector(config.GET_ENDPOINT, config.INTERVAL)
metrics_collector = AsyncWebsocketMetricsCollector(config.WS_ENDPOINT, config.INTERVAL)

async def main():
    while True:
        try:
            await loop()
        except Exception as e:
            print(e)
            g1.set_value(0)
            g2.set_value(0)
            g3.set_value(0)
            g4.set_value(0)
            await asyncio.sleep(config.RETRY_INTERVAL)
            
async def loop():
    async for metrics in metrics_collector:
        print(metrics)
        
        cpu_temp = metrics['cpu_temp']
        cpu_usage = metrics['cpu_usage']
        ram_usage = metrics['ram_usage']
        swap_usage = metrics['swap_usage']
            
            
        g1.set_value(cpu_usage / 100)
        g2.set_value(cpu_temp / 100)
        g3.set_value(ram_usage / 100)
        g4.set_value(swap_usage / 100)

asyncio.run(main())
