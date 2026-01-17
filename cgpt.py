#!/usr/bin/env python3

# Author - Act
# World Map ASCII Viewer

import os
import time

GREEN = "\033[92m"
CYAN = "\033[96m"
RESET = "\033[0m"

WORLD_MAP = f"""{CYAN}
                                 .-'''-.
                                '   _    \\
______   ______   ______      /   /` '.   \\
|    _ `''.\\    | |    |    .   |     \\  '
| _ | ) _  \\   | |    |    |   '      |  '
|( ''_'  ) |   | |    |    \\    \\     / /
| . (_) `. |   | |    |  _ `.   ` ..' / 
|(_    ._) '   | |    |.' |  '-...-'`
|  (_.\\.'  /    | |      /    ,----.
|       .'     | |     .    .'      \\
'----'`        | |   .'   .'\\  .--.  \\
               |_| .'   .'  |  |    |  '
                  '----'    '--'    '--'
""" + RESET

def banner():
    os.system("clear")
    print(GREEN + r"""
 __      __      _     _     _ 
 \ \    / /__ _ | |__ | |__ (_)
  \ \/\/ // _` || '_ \| '_ \| |
   \_/\_/ \__,_||_.__/|_.__/|_|
     WORLD MAP VIEWER
""" + RESET)

def show_map():
    banner()
    print(WORLD_MAP)
    print(GREEN + "\nZoom: Not Supported (ASCII Mode)" + RESET)
    print(CYAN + "Tip: Use fullscreen for best view.\n" + RESET)

def main():
    while True:
        banner()
        print(CYAN + "1) Show World Map" + RESET)
        print(CYAN + "2) About" + RESET)
        print(CYAN + "3) Exit\n" + RESET)

        choice = input(GREEN + "Select option: " + RESET)

        if choice == "1":
            show_map()
            input("\nPress Enter to return...")
        elif choice == "2":
            banner()
            print(GREEN + "Author: Act" + RESET)
            print("A simple ASCII world map viewer made in Python.")
            input("\nPress Enter to return...")
        elif choice == "3":
            print(GREEN + "Exiting..." + RESET)
            time.sleep(1)
            break
        else:
            print("Invalid option!")
            time.sleep(1)

if __name__ == "__main__":
    main()