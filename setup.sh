sudo apt-get update

sudo apt-get install -y git
sudo apt-get install -y couchdb
sudo apt-get install -y python-pip
sudo apt-get install -y python3-pip
sudo pip install flask
sudo pip install tornado
# required on ubuntu:
# http://stackoverflow.com/questions/21168141/cannot-install-packages-using-node-package-manager-in-ubuntu
sudo apt-get install -y nodejs-legacy
sudo apt-get install -y npm
sudo npm install gulp -g

# install python nmap library and also 
# calls a script that updates nmap's mac address prefixes
sudo pip-3.2 install python-libnmap
sudo pip-3.2 install tornado
update-nmap-mac-prefixes.sh
sudo cp /usr/share/nmap/nmap-mac-prefixes /usr/share/nmap/nmap-mac-prefixes.backup
sudo mv nmap-mac-prefixes /usr/share/nmap/nmap-mac-prefixes

# the following command sets up replication from the source database (local network) to the database production APIs use.
#curl -i \
#	-H "Content-Type: application/json" \
#    -X POST -d "{'_id':'local_location_services_homeToProduction', 'source':'<local network db>/local_location_services', 'target': 'local_location_services', 'create_target': true, 'continuous': true, 'user_ctx': {'roles': ['_admin']}' \
#    http://localhost:5984/_replicator


# copy config/globalConfigs.template to config/globalConfigs.js and fill in appropriate values

