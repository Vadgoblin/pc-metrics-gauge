import network
import secrets
from time import sleep

def connect(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    while not wlan.isconnected():
        sleep(0.2)
        
    try:
        wlan.config(pm=wlan.PM_POWERSAVE)
    except:
        print("failed to set power management profile for wifi")

    print("Successfully connected to the wifi")
    print(wlan.ifconfig())
