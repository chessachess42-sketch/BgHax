#!/bin/bash

# COLOR CODES
RED='\033[0;31m'
GRN='\033[0;32m'
YLW='\033[1;33m'
CYA='\033[0;36m'
RST='\033[0m'

clear

echo -e "${RED}"
echo "                 ███████████████████████████████████"
echo "                 █────█────█────█────█────█────█───█"
echo "                 █ Skull-Based IP Tracking System █"
echo "                 █────█────█────█────█────█────█───█"
echo "                 ███████████████████████████████████"
echo -e "${RST}"

sleep 1

echo -e "${RED}"
echo "                        ▄▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▄"
echo "                      ▄▀██████████████████▀▄"
echo "                     ████████████████████████"
echo "                    ██████████████████████████"
echo "                    ███████▀    ▀███▀    ▀████"
echo "                    ██████   ▄▀▀▄   ▄▀▀▄   ████"
echo "                    ██████   ▀▀▀▀   ▀▀▀▀   ████"
echo "                    ███████▄           ▄███████"
echo "                     ████████████████████████"
echo "                      ▀████████████████████▀"
echo "                         ▀▀████████████▀▀"
echo -e "${RST}"

sleep 1

echo -e "${YLW}Author = Act${RST}"
echo
sleep 1

echo -e "${RED}[ SYSTEM INITIALIZING ]${RST}"
sleep 1
echo -e "${RED}[ LOADING MODULES . . . ]${RST}"
sleep 1
echo -e "${RED}[ ESTABLISHING CONNECTION TO NETWORK NODES ]${RST}"
sleep 1
echo

read -p "Target IP: " IP

if [ -z "$IP" ]; then
    echo -e "${RED}[ ERROR ] No IP entered.${RST}"
    exit 1
fi

echo
echo -e "${YLW}Engaging Deep Scan Mode...${RST}"
sleep 1
echo -e "${CYA}Locating target across global network grids...${RST}"
sleep 1
echo -e "${RED}Compiling geolocation layers...${RST}"
sleep 1
echo -e "${GRN}Extracting ISP, Organization, and Node Routes...${RST}"
sleep 1
echo

data=$(curl -s https://ipinfo.io/$IP/json)

ip=$(echo $data | jq -r '.ip')
city=$(echo $data | jq -r '.city')
region=$(echo $data | jq -r '.region')
country=$(echo $data | jq -r '.country')
loc=$(echo $data | jq -r '.loc')
org=$(echo $data | jq -r '.org')
tz=$(echo $data | jq -r '.timezone')
postal=$(echo $data | jq -r '.postal')

echo -e "${RED}=========================================================${RST}"
echo -e "${GRN}                TARGET DATA DECODED${RST}"
echo -e "${RED}=========================================================${RST}"
echo -e "${YLW} IP Address          : ${CYA}$ip${RST}"
echo -e "${YLW} Country             : ${CYA}$country${RST}"
echo -e "${YLW} Region              : ${CYA}$region${RST}"
echo -e "${YLW} City                : ${CYA}$city${RST}"
echo -e "${YLW} Postal Code         : ${CYA}$postal${RST}"
echo -e "${YLW} Time Zone           : ${CYA}$tz${RST}"
echo -e "${YLW} Organization        : ${CYA}$org${RST}"
echo -e "${YLW} Coordinates         : ${CYA}$loc${RST}"
echo -e "${RED}=========================================================${RST}"
echo

sleep 1
echo -e "${CYA}Generating location grid reference link...${RST}"
sleep 1
echo "https://maps.google.com/?q=$loc"
echo
sleep 1

echo -e "${RED}[ PROCESS COMPLETE ]${RST}"