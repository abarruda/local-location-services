service cron start

chown -R couchdb:couchdb /data

su couchdb -c 'couchdb -b'
# give the database a change to start
while ! nc -vz localhost 5984; do sleep 1; done

/bin/sh create_dbs.sh
/bin/sh /views/install_views.sh

tail -n500 /var/log/couchdb/couch.log

# shutdown couchdb running in background
su couchdb -c 'couchdb -d'

# start couchdb in foreground so logging goes to stdout
su couchdb -c 'couchdb'
