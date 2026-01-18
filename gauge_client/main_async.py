from machine import Pin, PWM
from time import sleep
import network
import requests
import time
import wifi
import config
import uasyncio as asyncio
import uaiohttpclient as aiohttp
import json

from gauge import SmoothGauge

from metrics_collector import async_http_get_metrics_collector

#g1 = SimpleGauge(Pin(14), config.DUTY_CYCLE_4_GAUGE_100_PERCENT)
#g2 = SimpleGauge(Pin(15), config.DUTY_CYCLE_4_GAUGE_100_PERCENT)

g1 = SmoothGauge(Pin(14), config.DUTY_CYCLE_4_GAUGE_100_PERCENT)
g2 = SmoothGauge(Pin(15), config.DUTY_CYCLE_4_GAUGE_100_PERCENT)

class AsyncCounter:
    def __init__(self, limit):
        self.limit = limit
        self.current = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.current < self.limit:
            await asyncio.sleep_ms(200) # Yield control to the loop
            val = self.current
            self.current += 1
            return val
        else:
            # In MicroPython, you still raise StopIteration 
            # to signal the end of the loop
            raise StopAsyncIteration
        
class AsyncRange:
    def __init__(self, stop):
        self.i = 0
        self.stop = stop

    def __aiter__(self):
        return self

    # Notice: NO 'async' keyword here
    def __anext__(self):
        if self.i < self.stop:
            val = self.i
            self.i += 1
            # Return a coroutine that resolves to the value
            return self._wait_and_return(val)
        else:
            raise StopAsyncIteration
            # Raising StopIteration here is safe because it's a regular function
        #    raise StopIteration

    async def _wait_and_return(self, val):
        await asyncio.sleep_ms(100)
        return val
        
async def test():
    for i in range(5):
        await asyncio.sleep(1)
        yield i
        
async def async_range(count):
    for i in range(count):
        await asyncio.sleep_ms(500)  # Simulate an I/O task
        yield i

async def main():
    counter = AsyncCounter(5)
    async for num in counter:
        print("Counter:", num)
    print("ligma")
        
    #async for i in test():
    #   print(i)
        
    #async for stats in async_http_get_metrics_collector.iter_metrics(config.GET_ENDPOINT,3):
    #    print(stats)
    
    
    while True:
        try:
            a = time.ticks_ms()
            #stats = await get_data()
            stats = await async_http_get_metrics_collector.get_metrics(config.GET_ENDPOINT,3)
            b = time.ticks_ms()
            diffs = time.ticks_diff(b, a)
            print(f"{diffs-3000} ms to get data")
            
            #print(stats)
                
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
            await asyncio.sleep(config.INTERVAL)


asyncio.run(main())