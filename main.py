# 2022-12-07 @HTSpecOps
# Coffee Roaster Temperature Monitor Client
from utime import sleep
import urequests as requests
from machine import Pin, I2C
import adafruit_mcp9600
#from sh1107 import SH1107_I2C
import network
#import env var.
import config

# frequency must be set for the MCP9600 to function.
# If you experience I/O errors, try changing the frequency.
i2c = I2C(id=1, scl=Pin(27), sda=Pin(26), freq=100000)  # type: ignore
mcp = adafruit_mcp9600.MCP9600(i2c)
#display = SH1107_I2C(width=128, height=64, i2c=i2c)
led = Pin("LED", machine.Pin.OUT) # onbord LED

#temperature data store
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
    sleep(3) #added extra time to connecto to wifi

print(wlan.ifconfig())

# Init Display Label
#display.text("  Local | Probe", 0, 0, 1)
#display.show()

# HTTP REQUEST
def sendData(probeData):
    payload = {'probe': probeData }
    r = requests.post(url, json=payload)
    print('http %d' % r.status_code) #need to add timeout func for when server is down
    r.close()

while True:
    while wlan.isconnected():

        temp_ambiant = mcp.ambient_temperature * 1.8 + 32 #convert to Fahrenheit
        temp_probe = mcp.temperature * 1.8 +32
        print('ambiant : %d    probe : %d' % (round(temp_probe), round(temp_ambiant)))

        #display.fill_rect(20, 12, 120, 10, 0)
        #display.text(str(round(temp_ambiant)), 20, 14, 2)
        #display.text(str(round(temp_probe)), 82, 14, 2)
        #display.show()

        sendData(round(mcp.temperature))
        led.on()
    
        # DATA LOGGER
        #file.write(temp_ambiant + "," + temp_probe + "\r\n")
        #file.flush()
        sleep(1)
        led.off()