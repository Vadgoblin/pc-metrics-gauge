from machine import Pin, PWM
from time import sleep
import network
import secrets
import requests
import time


wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets.SSID, secrets.PASSWORD)
wlan.config(pm= wlan.PM_PERFORMANCE)

while not wlan.isconnected():
    sleep(0.2)

print("Successfully connected to the wifi")
print(wlan.ifconfig())

pwm1 = PWM(Pin(14))
pwm1.freq(10_000)

pwm2 = PWM(Pin(15))
pwm2.freq(10_000)

pwm1.duty_u16(0)
pwm2.duty_u16(0)

DUTY_CYCLE_4_GAUGE_100_PERCENT = 52_000

INTERVAL = 0.5

ENDPOINT = f"http://192.168.0.10:4972/stats?interval={INTERVAL}"


while True:
    try:
        a = time.ticks_ms()
        response = requests.get(ENDPOINT)
        b = time.ticks_ms()
        diffs = time.ticks_diff(b, a)
        print(diffs-(1000 * INTERVAL))
        
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
        
        pwm1.duty_u16(int(cpu_usage * DUTY_CYCLE_4_GAUGE_100_PERCENT / 100))
        pwm2.duty_u16(int(cpu_temp * DUTY_CYCLE_4_GAUGE_100_PERCENT / 100))
    except:  
        sleep(INTERVAL)