import os
import time
import requests

# Clear screen
os.system("clear")

# ==============================
# ASCII BANNER
# ==============================

skull = r"""
█████████████████████████████████████████████
█▄─▄███▄─█─▄█▄─▄▄─███▄─██─▄█▄─▀█▄─▄█─▄▄▄▄█
██─██▀██▄▀▄███─▄█▀████─██─███─█▄▀─██▄▄▄▄─█
▀▄▄▄▄▄▀▀▀▄▀▀▀▄▄▄▄▄▀▀▀▀▄▄▄▄▀▀▄▄▄▀▀▄▄▀▄▄▄▄▄▀

              ███████████████
           ███▀░░░░░░░░░░░░░▀███
        ██▀░░░░░░░░░░░░░░░░░░░░▀██
      ██░░░░░░░░░░░░░░░░░░░░░░░░░██
     ██░░░░░░░░░██░░░░██░░░░░░░░░██
     ██░░░░░░░░░████████░░░░░░░░░██
     ██░░░░░░░░░░██████░░░░░░░░░░██
      ██░░░░░░░░░░░░░░░░░░░░░░░██
        ██░░░░░░░░░░░░░░░░░░░██
           ███░░░░░░░░░░░░███
              █████████████
"""

print(skull)

# ==============================
# SYSTEM BOOT SEQUENCE
# ==============================

def stage(text, delay=0.7):
    print(f"[ {text} ]")
    time.sleep(delay)

print("Author : Act\n")

stage("SYSTEM INITIALIZING")
stage("BOOTING CORE PROTOCOLS")
stage("LOADING MODULES")
stage("LOCKING ONTO TARGET VECTOR")
stage("ENGAGING RECON ENGINE")

print()

# ==============================
# INPUT TARGET IP
# ==============================

ip = input("Target IP: ")

# ==============================
# API REQUEST
# ==============================

print("\n[ SCANNING NETWORK LAYERS ]\n")
time.sleep(1)

try:
    url = f"http://ip-api.com/json/{ip}"
    response = requests.get(url).json()

    if response["status"] == "success":
        print("=== RECON DATA STREAM ===\n")
        for key, value in response.items():
            print(f"{key.upper():15}: {value}")
    else:
        print("ERROR: Could not retrieve data. Target may be shielded.")
except Exception as e:
    print(f"Request Failed: {e}")

print("\nSCAN COMPLETE.")