import couchdb
from time import sleep

couchdb_url = 'http://localhost:5984/'
couchdb_name = 'test_tracker'

print "Reseting " + couchdb_name + " in 5 seconds..."
sleep(5)
couchServer = couchdb.Server(couchdb_url)
del couchServer[couchdb_name]
couchServer.create(couchdb_name)	
