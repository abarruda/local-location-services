# install python nmap library and also 
# calls a script that updates nmap's mac address prefixes

sudo pip-3.2 install python-libnmap
update-nmap-mac-prefixes.sh
sudo cp /usr/share/nmap/nmap-mac-prefixes /usr/share/nmap/nmap-mac-prefixes.backup
sudo mv nmap-mac-prefixes /usr/share/nmap/nmap-mac-prefixes

