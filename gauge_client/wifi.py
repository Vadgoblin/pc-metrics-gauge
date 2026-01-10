import network
import secrets

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets.SSID, secrets.PASSWORD)
wlan.config(pm= wlan.PM_PERFORMANCE)

while not wlan.isconnected():
    sleep(0.2)

print("Successfully connected to the wifi")
print(wlan.ifconfig())