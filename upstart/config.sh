rm /etc/init/local_location_services_api.conf
rm /etc/init.d/local_location_services_api

cp local_location_services_api.conf /etc/init/.
ln -s /etc/init/local_location_services_api.conf /etc/init.d/local_location_services_api
