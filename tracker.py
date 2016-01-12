import sys
from datetime import datetime
from time import sleep
from libnmap.process import NmapProcess
from libnmap.parser import NmapParser
from Host import Host
import couchdb
from couchdb import ResourceNotFound

couchdb_url = 'http://localhost:5984/'
couchdb_name = 'test_tracker'
HOST_IDLE_THRESHOLD_MINUTES = 15
SCAN_HEARTBEAT_SECONDS = 30

def scanNetwork(networkRange):
  print str(datetime.now()) + " - Scanning network for hosts..."
  nm = NmapProcess(targets=networkRange, options="-sP -n")
  nm.run()

  if nm.rc == 0:
    nmap_report = NmapParser.parse(nm.stdout)

    numHosts = 0
    detectedHosts = {}
    for host in nmap_report.hosts:
      if host.is_up():
        seen = datetime.now()
        detectedHost = Host(_id=host.mac, ip_address=host.ipv4, vendor=host.vendor)
        detectedHosts[detectedHost._id] = detectedHost
        numHosts += 1
    print "Number of hosts detected: " + str(numHosts)
    print ""
    return detectedHosts

  else:
    print(nm.stderr)

couch = couchdb.Server(couchdb_url)
db = couch[couchdb_name]

while True:
  try:
    # perform network scan
    detectedHosts = scanNetwork("192.168.1.2-99")
    # establish a timestamp that will be used for all updates for this scan
    scanTimestamp = datetime.now()

    # update existing tracked hosts last_seen or insert new record for each new host
    for key, host in detectedHosts.items():
      hostRecord = host.load(db, key)

      if hostRecord is not None:
        hostRecord.update(scanTimestamp, host.ip_address, host.vendor) 
        hostRecord.store(db)
      else:
        print("Tracking hew host: " + host.identString())
        host.first_seen = scanTimestamp
        host.last_seen = scanTimestamp
        host.activate(scanTimestamp)
        host.recordIp()
        host.store(db)


    # iterate over all currently tracked hosts
    # TODO: maintain a list of ids above and remove them from the list
    # we're about to iterate over
    for id in db:
      if id[0] != "_": # ignore design document ("_design/tracker")
        trackedHost = Host.load(db, id)

        # determine if the host is INACTIVE and update
        if trackedHost.isInactivateWithIdleTime(scanTimestamp, HOST_IDLE_THRESHOLD_MINUTES):
          trackedHost.inactivate()
          trackedHost.store(db)

    # compact DB to remove revisions we don't need
    db.compact()
  except:
    print "Unexpected error:", sys.exc_info()

  sys.stdout.flush()
  sleep(SCAN_HEARTBEAT_SECONDS)
