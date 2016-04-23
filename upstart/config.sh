rm /etc/init/tracker_api.conf
rm /etc/init.d/tracker_api

cp tracker_api.conf /etc/init/.
ln -s /etc/init/tracker_api.conf /etc/init.d/tracker_api
