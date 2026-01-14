#!/usr/bin/env python3

import requests
import os
import time

GREEN = "\033[92m"
CYAN = "\033[96m"
RESET = "\033[0m"

def banner():
    os.system("clear")
    print(GREEN + r"""
 _   _    _    _____ 
| \ | |  / \  |_   _|
|  \| | / _ \   | |  
| |\  |/ ___ \  | |  
|_| \_/_/   \_\ |_|  
""" + RESET)
    print(CYAN + " IP INFORMATION TRACKER" + RESET)
    print(GREEN + " Author - Act" + RESET)
    print()
    print(GREEN + "[1] Lookup your own IP")
    print("[2] Lookup custom IP")
    print("[3] Exit" + RESET)
    print()

def lookup(ip=None):
    try:
        url = "http://ip-api.com/json/" + (ip if ip else "")
        data = requests.get(url).json()

        print(GREEN + "\n--- IP INFORMATION ---\n" + RESET)
        for k, v in data.items():
            print(f"{GREEN}{k.upper():15}{RESET} : {v}")
        print()
    except:
        print("Error fetching data!")

while True:
    banner()
    choice = input(GREEN + "Select option > " + RESET)

    if choice == "1":
        lookup()
        input("\nPress Enter to continue...")
    elif choice == "2":
        custom = input(GREEN + "Enter IP address: " + RESET)
        lookup(custom)
        input("\nPress Enter to continue...")
    elif choice == "3":
        print(GREEN + "\nExiting..." + RESET)
        time.sleep(1)
        break
    else:
        print("Invalid choice!")
        time.sleep(1)