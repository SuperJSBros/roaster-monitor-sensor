# 2022-12-07 @HTSpecOps
# 2025-05-25 @HTSpecOps restarted working on this project
# Coffee Roaster Temperature Monitor Client
import asyncio
import network
from machine import Pin, I2C
import requests
import adafruit_mcp9600
import time
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
# plain header is used when the data format is Influxdb type
headers = {'Content-Type': 'text/plain'}
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
def sendData(payload):
    # res = requests.post(url, data=payload, timeout=5))
    # print('http %d   payload: %s' % (res.status_code, payload)) #need to add timeout func for when server is down
    # led.off() if res.status_code != 204 else led.on()
    # res.close()
    try:
        res = requests.post(url, data=payload, timeout=10)
        print('http %d payload: %s' % (res.status_code, payload))
        led.off() if res.status_code != 204 else led.on() # Turn off LED if not 204 (No Content), else turn it on
        res.close()
        return  # Success, exit the function
    except OSError as e:
            print("Failed to send data due to OSError: %s" %  e)
    
def sample_data():

    temp_ambiant = mcp.ambient_temperature * 1.8 + 32  # convert to Fahrenheit
    temp_probe = mcp.temperature * 1.8 + 32
    #print('ambiant : %d    probe : %d' % (round(temp_probe), round(temp_ambiant)))

    payload = "roast,roaster_id=" + str(config.ROASTER_ID) + " temp_ambiant=" + str(round(temp_ambiant)) + ",temp_probe=" + str(round(temp_probe))
    sendData(payload)

while True:
    while wlan.isconnected():

        sample_data()
    
        # DATA LOGGER
        #file.write(temp_ambiant + "," + temp_probe + "\r\n")
        #file.flush()
        time.sleep(2)