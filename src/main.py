# main.py
from machine import SoftSPI, Pin, idle
import tinypico as TinyPICO
from dotstar import DotStar
import time, random, micropython
from network import WLAN, STA_IF, 
import urequests 
import json
import ntptime

def load_config():
	try:
		with open('config.json',"r") as data_file:
			data = json.load(data_file)
			config = {
				"ssid": data["network"]["ssid"],
                "key": data["network"]["key"],
                "username": data["github"]["username"],
                "token": data["github"]["token"]
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

def get_time():
    # TODO: Add timezone to config or auto populate using ip address.
    url = "https://timeapi.io/api/Time/current/zone?timeZone=America/Ensenada"
    response = urequests.get(url)
    json_response = response.json()
    print(json_response)

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

# def graph_ql(user, token):
#     url = "https://api.github.com/graphql"
#     headers = {
#         "Authorization":"token {}".format(token),
#         "Accept":"application/vnd.github.mercy-preview+json",
#         'User-Agent': 'My User Agent 1.0'
#     }
#     query = """
#         query {
#         user(login: "USERNAME") {
#             contributionsCollection {
#             contributionCalendar {
#                 totalContributions
#                 weeks {
#                 contributionDays {
#                     date
#                     contributionCount
#                   }
#                 }
#               }
#             }
#           }
#         }
#         """
#     request = urequests.post(url=url,headers=headers,json={'query':query})
#     json_request = request.json()
#     data = json_request["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
#     len_data = len(data)
#     latest_week = json_request["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"][len_data-1]["contributionDays"]
#     len_latest_week = (len(latest_week)-1)
#     cur_day = latest_week[len_latest_week]

#     if((cur_day["contributionCount"])):
#         print(True)
#     else:
#         print(False)

def get_latest_commit(user, token):
    search_url = "https://api.github.com/search/repositories?q=user:" + user
    headers = {"Authorization":"token {}".format(token),'User-Agent': 'My User Agent 1.0'}
    response = urequests.get(search_url, headers=headers)
    search_results = response.json()
    print(search_results)

    # total_pages = search_results['total_pages']

    # for page in range(1, total_pages + 1):
    #     search_url = "https://api.github.com/search/repositories?q=user:{user}&page={page}"
    #     response = urequest.get(search_url, headers=headers)
    #     print(response.json())
    #     search_results = response.json()

    #     for item in search_results['items']:
    #         repo_name = item['name']
    #         commits_url = "https://api.github.com/repos/{user}/{repo_name}/commits"

    #         # Make a urequest to get the repository commits
    #         response = urequest.get(commits_url, headers=headers)
    #         commits = response.json()

    #         # Check if there are any commits in the repository
    #         if len(commits) > 0:
    #             latest_commit = commits[0]["sha"]
    #             print(f"Latest commit in repository {repo_name}: {latest_commit}")

# Replace 'your_username' with the GitHub username you want to retrieve the commits for
# Replace 'your_token' with your personal access token
do_connect(config["ssid"], config["key"])
# get_latest_commit(config["username"], config["token"])
# graph_ql(config["username"], config["token"])
# Say hello

get_time()

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
