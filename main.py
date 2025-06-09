# 2022-12-07 @HTSpecOps
# 2025-05-25 @HTSpecOps restarted working on this project
# Coffee Roaster Temperature Monitor Client
import asyncio
import network
from machine import Pin, I2C
import requests
import adafruit_mcp9600
import time
import json
#import env var.
import config

# frequency must be set for the MCP9600 to function.
# If you experience I/O errors, try changing the frequency.
i2c = I2C(id=1, scl=Pin(27), sda=Pin(26), freq=100000)  # type: ignore
mcp = adafruit_mcp9600.MCP9600(i2c)
led = Pin("LED", machine.Pin.OUT) # onbord LED

#temperature data store - for use as a logger
# file = open("data.csv", "w")

# URL for backend route
url = config.URL
print(url)

# Connect To Wifi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
while not wlan.isconnected():
    wlan.connect(config.WLAN_ID, config.WLAN_PASS)
    print("Waiting to connect to %s" % config.WLAN_ID)
    time.sleep(3)

print(wlan.ifconfig())

# HTTP REQUEST
def sendData(): #require json format
    
    payload = config.SETTINGS  # Use the settings from config.py
    payload.update({
        "temperature": {
            "ambient": mcp.ambient_temperature * 1.8 + 32,  # convert to Fahrenheit
            "probe": mcp.temperature * 1.8 + 32
        }
    })
    
    try:
        res = requests.post(url, json=payload, timeout=10)
        print('http %d payload: %s' % (res.status_code, json.dumps(payload)))
        led.off() if res.status_code != 204 else led.on() # Turn off LED if not 204 (No Content), else turn it on
        res.close()
        return  # Success, exit the function
    except OSError as e:
            print("Failed to send data due to OSError: %s" %  e)
    

while True:
    while wlan.isconnected():
        
        sendData()
        # DATA LOGGER
        #file.write(temp_ambiant + "," + temp_probe + "\r\n")
        #file.flush()
        time.sleep(2)