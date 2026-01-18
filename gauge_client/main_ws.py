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
from async_websocket_client import AsyncWebsocketClient



g1 = SmoothGauge(Pin(14), config.DUTY_CYCLE_4_GAUGE_100_PERCENT)
g2 = SmoothGauge(Pin(15), config.DUTY_CYCLE_4_GAUGE_100_PERCENT)


async def main():
    interval = 0.5
    
    asd = AsyncWebsocketClient()
    await asd.open()
    await asd.handshake(config.WS_ENDPOINT)
    await asd.send('{"interval": '+str(interval) +'}')
    
    
    import usocket
    #asd.sock.setsockopt(usocket.IPPROTO_TCP, usocket.TCP_NODELAY, 1)


    while True:
        i = await asd.recv()
        print(i)
        
    last_time = time.ticks_ms()

    while True:
        try:
            i = await asd.recv()
            if i is not None:
                # 1. Capture current time
                current_time = time.ticks_ms()
                
                # 2. Calculate difference (delta)
                # ticks_diff handles the rollover of the internal counter
                diff = time.ticks_diff(current_time, last_time)
                
                #print(f"Msg: {i} | Time since last: {diff}ms")
                print(interval*1000-diff)
                
                # 3. Update last_time for the next iteration
                last_time = current_time
                
        except Exception as e:
            print(f"Error receiving: {e}")
            break
    
    asdasd
    
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
