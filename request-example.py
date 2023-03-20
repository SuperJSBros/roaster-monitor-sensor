import network
import utime
#import env var.
import config

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(config.WLAN_ID, config.WLAN_PASS)

while not wlan.isconnected() and wlan.status() >= 0:
    print("Waiting to connect:")
utime.sleep(1)
print(wlan.ifconfig())

#HTTP REQUEST
import urequests
import random
while True:
    ambient = random.randrange(0,100,1)
    url = "http://192.168.1.10:3000/daily-probes"
    payload = {
        'probe': ambient
    }
    print(url)
    r = urequests.post(url, json=payload)
    print(r.status_code) #need to add timeout func for when server is down
    utime.sleep(1)
    r.close()