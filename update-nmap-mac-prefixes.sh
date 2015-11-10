#!/bin/bash
# update_mac_addresses.sh
# This script downloads the currect mac address data from the IEEE and parses it for nmap and arpwatch.
# nmap-mac-prefixes is for nmap.
# modified from the version here (no arp): http://giantdorks.org/alain/script-to-update-nmap-mac-prefixes-with-latest-entries-from-the-ieee-oui-database/

# Run the following commands when this script completes:
# sudo cp /usr/share/nmap/nmap-mac-prefixes /usr/share/nmap/nmap-mac-prefixes.backup
# sudo mv nmap-mac-prefixes /usr/share/nmap/nmap-mac-prefixes


# Download the current data

#wget http://standards.ieee.org/regauth/oui/oui.txt
wget http://standards-oui.ieee.org/oui.txt

# Divide the data into Manufacturer and Address files
cat oui.txt | grep '(base 16)' | cut -f3 > mac.manufacturer 
cat oui.txt | grep '(base 16)' | cut -f1 -d' ' > mac.address 



# Paste them back together for nmap data 
paste mac.address mac.manufacturer > nmap-mac-prefixes

# Clean up intermediary files
rm tmp.address
rm mac.address
rm mac.manufacturer
rm oui.txt
