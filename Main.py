import os, time, requests, json

# ANSI COLORS
RED = "\033[31m"
GRN = "\033[32m"
YLW = "\033[33m"
CYA = "\033[36m"
RST = "\033[0m"

os.system("clear")

# SKULL ASCII
print(RED + """
                 ███████████████████████████████████
                 █────█────█────█────█────█────█───█
                 █   SKULL-BASED IP RECON SYSTEM   █
                 █────█────█────█────█────█────█───█
                 ███████████████████████████████████

                        ▄▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▄
                      ▄▀██████████████████▀▄
                     ████████████████████████
                    ██████████████████████████
                    ███████▀    ▀███▀    ▀████
                    ██████   ▄▀▀▄   ▄▀▀▄   ████
                    ██████   ▀▀▀▀   ▀▀▀▀   ████
                    ███████▄           ▄███████
                     ████████████████████████
                      ▀████████████████████▀
                         ▀▀████████████▀▀
""" + RST)

print(YLW + "Author: Act" + RST)
time.sleep(1)

# LOADING SEQUENCE
seq = [
    "[ SYSTEM INITIALIZING ]",
    "[ LOADING CORE MODULES ]",
    "[ ESTABLISHING ROUTING NODES ]",
    "[ ENGAGING DEEP SCAN ]"
]

for s in seq:
    print(RED + s + RST)
    time.sleep(0.9)

print()

# INPUT
ip = input(YLW + "Target IP: " + RST)

if ip.strip() == "":
    print(RED + "No IP entered. Exiting." + RST)
    exit()

print()
print(CYA + "Locating target across global grids..." + RST)
time.sleep(1)
print(RED + "Compiling geolocation layers..." + RST)
time.sleep(1)
print(GRN + "Extracting ISP / Organization / Timezone..." + RST)
time.sleep(1)
print()

# FETCH INFO
try:
    data = requests.get(f"https://ipinfo.io/{ip}/json").json()
except:
    print(RED + "Connection error. Cannot fetch data." + RST)
    exit()

ip_addr = data.get("ip", "N/A")
city = data.get("city", "N/A")
region = data.get("region", "N/A")
country = data.get("country", "N/A")
loc = data.get("loc", "N/A")
org = data.get("org", "N/A")
postal = data.get("postal", "N/A")
timezone = data.get("timezone", "N/A")

# OUTPUT
print(RED + "=========================================================" + RST)
print(GRN + "                TARGET DATA DECODED" + RST)
print(RED + "=========================================================" + RST)

print(YLW + " IP Address          : " + CYA + ip_addr + RST)
print(YLW + " Country             : " + CYA + country + RST)
print(YLW + " Region              : " + CYA + region + RST)
print(YLW + " City                : " + CYA + city + RST)
print(YLW + " Postal Code         : " + CYA + postal + RST)
print(YLW + " Time Zone           : " + CYA + timezone + RST)
print(YLW + " Organization        : " + CYA + org + RST)
print(YLW + " Coordinates         : " + CYA + loc + RST)

print(RED + "=========================================================" + RST)
print()

time.sleep(1)
print(CYA + "Generated Google Maps link:" + RST)
print("https://maps.google.com/?q=" + loc)
print()
time.sleep(1)

print(RED + "[ PROCESS COMPLETE ]" + RST)