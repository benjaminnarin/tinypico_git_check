# main.py
from machine import SoftSPI, Pin, idle
import tinypico as TinyPICO
from dotstar import DotStar
import time, random, micropython
from network import WLAN, STA_IF, 
import json

def load_config():
	try:
		with open('config.json',"r") as data_file:
			data = json.load(data_file)
			config = {
				"ssid": data["network"]["ssid"],
                "key": data["network"]["key"],
                "token": data["token"]
            }
			return config
	except:
		print("ERROR reading config file")
		return []

config = load_config()
# Setup Wireless Interface
wlan = WLAN(STA_IF)
wlan.active(True) # activate the interface

# Configure SPI for controlling the DotStar
# Internally we are using software SPI for this as the pins being used are not hardware SPI pins
spi = SoftSPI(sck=Pin( TinyPICO.DOTSTAR_CLK ), mosi=Pin( TinyPICO.DOTSTAR_DATA ), miso=Pin( TinyPICO.SPI_MISO) )
# Create a DotStar instance
dotstar = DotStar(spi, 1, brightness = 0.5 ) # Just one DotStar, half brightness
# Turn on the power to the DotStar
TinyPICO.set_dotstar_power( True )

dotstar[0] = ( 150, 0, 150, 0.05)

def do_connect(ssid: str, key: str):
    wlan.active(True) # activate the interface
    if not wlan.isconnected(): # check if the station is connected to an AP
        print('Connecting to network...') 
        wlan.connect(ssid, key) # connect to an AP
        while not wlan.isconnected(): # wait till we are really connected
            print('.', end='')
            time.sleep(0.1) #  you can also just put pass here
        print()
        print('Connected:', wlan.isconnected())
    else:
        print("Already connected!")
    # get the interface's IP/netmask/gw/DNS addresses
    print(wlan.ifconfig())

do_connect(config["ssid"], config["key"])

# Say hello
print("\nHello from TinyPICO!")
print("--------------------\n")

# Show some info on boot
print("Battery Voltage is {}V".format( TinyPICO.get_battery_voltage() ) )
print("Battery Charge State is {}\n".format( TinyPICO.get_battery_charging() ) )

# Show available memory
print("Memory Info - micropython.mem_info()")
print("------------------------------------")
micropython.mem_info()

# Rainbow colours on the Dotstar
while True:
    # Set the colour on the dotstar
    dotstar[0] = ( 150, 0, 0, 0.05)
    # Increase the wheel index
    # Sleep for 20ms so the colour cycle isn't too fast
    time.sleep_ms(20)
