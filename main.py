# 2022-12-07 @HTSpecOps
# Coffee Roaster Temperature Monitor Client
from utime import sleep
import urequests as requests
from machine import Pin, I2C, ADC
import adafruit_mcp9600
from sh1107 import SH1107_I2C
import network
#import env var.
import config


# frequency must be set for the MCP9600 to function.
# If you experience I/O errors, try changing the frequency.
i2c = I2C(id=1, scl=Pin(15), sda=Pin(14), freq=100000)  # type: ignore
mcp = adafruit_mcp9600.MCP9600(i2c, 60)
display = SH1107_I2C(width=128, height=64, i2c=i2c)

#temperature data store
# file = open("data.csv", "w")

# URL for backend route
url = "http://192.168.1.10:3000/daily-probes"
print(url)

# connect to Wifi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(config.WLAN_ID, config.WLAN_PASS)
while not wlan.isconnected() and wlan.status() >= 0:
    print("Waiting to connect:")
sleep(1)
print(wlan.ifconfig())

# display label
display.text("  Local | Probe", 0, 0, 1)
display.show()

# HTTP REQUEST
def sendData(probeData):
    payload = {
        'probe': probeData
    }
    
    r = requests.post(url, json=payload)
    print(r.status_code) #need to add timeout func for when server is down
    r.close()

while True:
    temp_ambiant = (str(mcp.ambient_temperature).split("."))[0]
    temp_probe = (str(mcp.temperature).split("."))[0]
    # print(temp_ambiant, temp_probe)
    print('probe temperature is %d' % round(mcp.temperature))

    display.fill_rect(20, 12, 120, 10, 0)
    display.text(temp_ambiant, 20, 12, 2)
    display.text(temp_probe, 82, 12, 2)
    display.show()

    sendData(round(mcp.temperature))

    #file.write(temp_ambiant + "," + temp_probe + "\r\n")
    #file.flush()
    sleep(1)


