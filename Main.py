import requests
import os
import time
import sys

CYAN  = "\033[96m"
GREEN = "\033[92m"
RESET = "\033[0m"
RED   = "\033[91m"

def clear():
    os.system("clear")

def slow(text, delay=0.02):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def banner():
    print(CYAN + "==============================================")
    print("        ███╗   ██╗ █████╗  ████████╗")
    print("        ████╗  ██║██╔══██╗ ╚══██╔══╝")
    print("        ██╔██╗ ██║███████║    ██║   ")
    print("        ██║╚██╗██║██╔══██║    ██║   ")
    print("        ██║ ╚████║██║  ██║    ██║   ")
    print("        ╚═╝  ╚═══╝╚═╝  ╚═╝    ╚═╝   ")
    print("==============================================" + RESET)
    print(GREEN + "            IP INFORMATION TRACKER\n" + RESET)

def loading():
    for i in range(3):
        sys.stdout.write(GREEN + "[*] Loading" + "." * (i+1) + "   \r")
        sys.stdout.flush()
        time.sleep(0.4)
    print(RESET)

def get_ip():
    try:
        loading()
        ip = requests.get("https://api.ipify.org").text
        return ip
    except:
        return None

def lookup(ip):
    try:
        url = f"https://ipapi.co/{ip}/json/"
        return requests.get(url).json()
    except:
        return None

def show_info(info):
    print(CYAN + "\n------------ RESULTS ------------" + RESET)
    for key, val in info.items():
        print(f"{GREEN}{key}: {CYAN}{val}{RESET}")
    print(CYAN + "----------------------------------" + RESET)

def menu():
    print(GREEN + "\n[1] Lookup your own IP")
    print("[2] Lookup custom IP")
    print("[3] Exit\n" + RESET)

# Main Program
clear()
banner()

while True:
    menu()
    choice = input(GREEN + "Select option > " + RESET)

    if choice == "1":
        ip = get_ip()
        if ip is None:
            print(RED + "Error fetching IP." + RESET)
        else:
            print(GREEN + f"\nYour IP: {CYAN}{ip}" + RESET)
            info = lookup(ip)
            show_info(info)

    elif choice == "2":
        target = input(GREEN + "Enter IP address: " + RESET)
        info = lookup(target)
        if info:
            show_info(info)
        else:
            print(RED + "Invalid IP or network error." + RESET)

    elif choice == "3":
        slow(CYAN + "Exiting…" + RESET)
        break

    else:
        print(RED + "Invalid choice!" + RESET)