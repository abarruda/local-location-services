import sys
import os
from datetime import datetime, timedelta
from time import sleep
import couchdb
from couchdb import ResourceNotFound
from Host import Host
from Event import Event
#from ScanUtils import ScanUtils
import ConfigParser
import traceback

if len(sys.argv) < 2:
  print "A property file must be specified to start scanner!"
  sys.exit(1)

configFile = sys.argv[1]
if not os.path.isfile(configFile):
  print "Property file does not exist, cannot start scanner!"
  sys.exit(1)

print "Using configuration file: " + configFile
config = ConfigParser.ConfigParser()
config.read(configFile)

couchdb_url = config.get('database', 'COUCHDB_URL')
couchdb_name = config.get('database', 'COUCHDB_SCANNER_NAME')
historical_db_name = config.get('database', 'COUCHDB_SCANNER_HISTORICAL_NAME')
HOST_IDLE_THRESHOLD_MINUTES = config.getint('scanner', 'HOST_IDLE_THRESHOLD_MINUTES')
SCAN_HEARTBEAT_SECONDS = config.getint('scanner', 'SCAN_HEARTBEAT_SECONDS')
HOST_IDLE_FOR_PING_MINUTES = config.getint('scanner', 'HOST_IDLE_FOR_PING_MINUTES')
SCAN_TYPE = config.get('scanner', 'SCANNER_TYPE')

if SCAN_TYPE == 'nmap':
  print("Scanner type: NMAP")
  from NmapScanUtils import NmapScanUtils
  scannerUtils = NmapScanUtils(config=config)

elif SCAN_TYPE == 'snmp':
  print("Scanner type: SNMP")
  from SnmpScanUtils import SnmpScanUtils
  scannerUtils = SnmpScanUtils(config=config)

couch = couchdb.Server(couchdb_url)
try:
  db = couch[couchdb_name]
except couchdb.http.ResourceNotFound:
  db = couch.create(couchdb_name)

try:
  historical_db = couch[historical_db_name]
except couchdb.http.ResourceNotFound:
  historical_db = couch.create(historical_db_name)

def recordEvent(timestamp, hostId, status):
  print "**** Recording event: " + str(timestamp) + " " + str(hostId) + " " + str(status)
  newEvent = Event(timestamp=timestamp, host_id=hostId, status=status)
  newEvent.store(historical_db)


while True:
  try:
    # perform network scan
    scanStart = datetime.now()
    detectedHosts = scannerUtils.scanNetwork()
    scanTime = datetime.now() - scanStart
    print "Number of hosts detected: " + str(len(detectedHosts)) + " (scan time: " + str(scanTime) + ")"

    # establish a timestamp that will be used for all updates for this scan
    scanTimestamp = datetime.now().replace(microsecond=0)
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
      # ignore design documents ("_design/local_location_services") and hosts we just detected
      if (id[0] != "_") and (id not in detectedHosts):
        trackedHost = Host.load(db, id)

        # if the host is ACTIVE, then it didn't come up in the nmap scan
        # perform a ping with last known IP.
        if trackedHost.isActive() and Host.isIdleFor(trackedHost, scanTimestamp, HOST_IDLE_FOR_PING_MINUTES):
          response, message, pingTime = scannerUtils.pingAndVerifyMacAddress(trackedHost.ip_address, trackedHost._id)
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
    traceback.print_exception(*sys.exc_info())

  sys.stdout.flush()
  sleep(SCAN_HEARTBEAT_SECONDS)
