import sys
from datetime import datetime, timedelta
from time import sleep
import couchdb
from couchdb import ResourceNotFound
from Host import Host
from Event import Event
from ScanUtils import ScanUtils

couchdb_url = 'http://localhost:5984/'
couchdb_name = 'test_tracker'
historical_db_name = 'tracker_historical'
HOST_IDLE_THRESHOLD_MINUTES = 15
SCAN_HEARTBEAT_SECONDS = 30
HOST_IDLE_FOR_PING_MINUTES = 5

couch = couchdb.Server(couchdb_url)
db = couch[couchdb_name]
historical_db = couch[historical_db_name]

def recordEvent(timestamp, hostId, status):
  print "**** Recording event: " + str(timestamp) + " " + str(hostId) + " " + str(status)
  newEvent = Event(timestamp=timestamp, host_id=hostId, status=status)
  newEvent.store(historical_db)


while True:
  try:
    # perform network scan
    detectedHosts = ScanUtils.scanNetwork("192.168.1.2-99")
    # establish a timestamp that will be used for all updates for this scan
    scanTimestamp = datetime.now()
    # update existing tracked hosts last_seen or insert new record for each new host
    for key, host in detectedHosts.items():
      hostRecord = host.load(db, key)

      if hostRecord is not None:
        if hostRecord.isInactive():
          recordEvent(scanTimestamp, key, Host.STATUS_ACTIVE)

        hostRecord.update(scanTimestamp, host.ip_address, host.vendor) 
        hostRecord.store(db)
        
      else:
        print("Tracking hew host: " + host.identString())
        host.first_seen = scanTimestamp
        host.last_seen = scanTimestamp
        host.activate(scanTimestamp)
        host.recordIp()
        host.store(db)
        recordEvent(scanTimestamp, key, Host.STATUS_ACTIVE)

    # iterate over all currently tracked hosts
    for id in db:
      # ignore design documents ("_design/tracker") and hosts we just detected
      if (id[0] != "_") and (id not in detectedHosts):
        trackedHost = Host.load(db, id)

        # if the host is ACTIVE, then it didn't come up in the nmap scan
        # perform a ping with last known IP.
        if trackedHost.isActive() and Host.isIdleFor(trackedHost, scanTimestamp, HOST_IDLE_FOR_PING_MINUTES):
          response, message, pingTime = ScanUtils.pingAnVerifyMacAddress(trackedHost.ip_address, trackedHost._id)
          print trackedHost.identString() + " " + message + " (ping time: " + str(pingTime) + ")"
          if response:
            trackedHost.update(scanTimestamp, trackedHost.ip_address, trackedHost.vendor)
            trackedHost.store(db)
            continue

        # determine if the host is INACTIVE and update
        if trackedHost.isInactiveWithIdleTime(scanTimestamp, HOST_IDLE_THRESHOLD_MINUTES):
          trackedHost.inactivate()
          trackedHost.store(db)
          # use the last seen timestamp when going INACTIVE, unless the timestamp
          # was also the timestamp for the last event (occurs when the host is 
          # detected only during one cycle), in which case add a second
          TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
          lastEventTime = datetime.strptime(trackedHost.last_event['timestamp'], TIME_FORMAT)
          if lastEventTime == trackedHost.last_seen:
            print "Host detected for one cycle, adding 1 second."
            eventTime = trackedHost.last_seen + timedelta(seconds = 1)
          else: 
            eventTime = trackedHost.last_seen
          recordEvent(eventTime, id, Host.STATUS_INACTIVE)

    # compact DB to remove revisions we don't need
    db.compact()
    print ""
    print ""
  except:
    print "Unexpected error:", sys.exc_info()

  sys.stdout.flush()
  sleep(SCAN_HEARTBEAT_SECONDS)
