import network
import secrets
from time import sleep

def connect(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    wlan.config(pm=wlan.PM_POWERSAVE)

    while not wlan.isconnected():
        sleep(0.2)

    print("Successfully connected to the wifi")
    print(wlan.ifconfig())
