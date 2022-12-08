# 2022-12-07 @HTSpecOps
# Coffee Roaster Temperature Monitor Client

from utime import sleep
import math
from machine import Pin, I2C
import adafruit_mcp9600
from sh1107 import SH1107_I2C

# frequency must be set for the MCP9600 to function.
# If you experience I/O errors, try changing the frequency.
i2c = I2C(id=1, scl=Pin(15), sda=Pin(14), freq=100000)  # type: ignore
mcp = adafruit_mcp9600.MCP9600(i2c, 96, "K", 0)
display = SH1107_I2C(128, 64, i2c)

#temperature data store
file = open("data.txt", "w")

#display label
display.text("  Local | Probe", 0, 0, 1)
while True:
    temp_ambiant = round(mcp.ambient_temperature, 1)
    temp_probe = round(mcp.temperature, 1)
    temp_delta = round(mcp.delta_temperature, 1)
    print((temp_ambiant, temp_probe, temp_delta))

    display.fill_rect(20, 15, 120, 10, 0)
    display.text(str(temp_ambiant), 20, 15, 2)
    display.text(str(temp_probe), 82, 15, 2)
    display.show()

    #file.write(str(temp_ambiant) + "," + str(temp_probe) + "\r\n")
    #file.flush()
    sleep(1)
