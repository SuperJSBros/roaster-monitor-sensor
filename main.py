# 2022-12-07 @HTSpecOps
# Coffee Roaster Temperature Monitor Client

from utime import sleep
import math
from machine import Pin, I2C
import adafruit_mcp9600

# frequency must be set for the MCP9600 to function.
# If you experience I/O errors, try changing the frequency.
i2c = I2C(id=1, scl=Pin(15), sda=Pin(14), freq=100000)  # type: ignore
mcp = adafruit_mcp9600.MCP9600(i2c, 96, "K", 0)
#temperature data store
file = open("data.txt", "w")

while True:
    temp_ambiant = round(mcp.ambient_temperature, 1)
    temp_probe = round(mcp.temperature, 1)
    temp_delta = round(mcp.delta_temperature, 1)
    print((temp_ambiant, temp_probe, temp_delta))
    file.write(str(temp_ambiant) + "," + str(temp_probe) + "\r\n")
    file.flush()
    sleep(1)
