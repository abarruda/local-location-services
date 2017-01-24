service couchdb start
# give the database a change to start
sleep 5
echo "Installing views..."
curl -X PUT http://localhost:5984/local_location_services
curl -X PUT http://localhost:5984/local_location_services_historical
# js file below must be specified as absolute path
curl -X PUT -d @/views/local_location_services_views.js 'http://localhost:5984/local_location_services/_design/local_location_services'
curl -X PUT -d @/views/local_location_services_historical_views.js 'http://localhost:5984/local_location_services_historical/_design/local_location_services_historical'
# without the sleep, views weren't persisting to the db.  Perhaps not enough time to commit to disk?
sleep 5
tail -n500 /var/log/couchdb/couch.log
service couchdb stop
