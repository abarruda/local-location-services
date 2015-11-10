# Class represents an Host that has connected to
# the network that is being tracked

from datetime import datetime
from datetime import timedelta
from couchdb.mapping import Document, TextField, DateTimeField, DictField

class Host(Document):
    _id = TextField()
    ip_address = TextField()
    vendor = TextField()
    name = TextField()
    status = TextField(default="ACTIVE")
    first_seen = DateTimeField(default=datetime.now)
    last_seen = DateTimeField(default=datetime.now)
    ip_address_history = DictField()
    event_history = DictField()

    def update(self, ip_address, vendor):
      self.last_seen = datetime.now()
      self.ip_address = ip_address
      self.recordIp()

      if self.status == 'INACTIVE':
          self.activate()

    def activate(self):
        print self.identString() + " has become ACTIVE"
        self.status = 'ACTIVE'
        self.event_history[str(datetime.now())] = self.status

    def inactivate(self):
        self.status = 'INACTIVE'
        self.event_history[str(self.last_seen)] = self.status

    def recordEvent(self, status):
        self.status = status
        self.event_history[str(datetime.now())] = status

    def recordIp(self):
        if self.ip_address in self.ip_address_history:
            currentValue = self.ip_address_history[str(self.ip_address)]
            self.ip_address_history[str(self.ip_address)] = currentValue + 1
        else:
            self.ip_address_history[str(self.ip_address)] = 1

    def isInactivateWithIdleTime(self, minutes):
        # if host is past the idle threshold, mark INACTIVE
        idleTimeSeconds = (datetime.now()-self.last_seen).total_seconds()
        if (self.status == 'ACTIVE' and idleTimeSeconds > (minutes*60)):
            idleMinutes, idleSeconds = divmod(idleTimeSeconds, 60)
            print(self.identString() + " has gone INACTIVE (" + \
                 str(idleMinutes) + " minutes, " + \
                 str(idleSeconds) + " seconds)")
            #self.recordEvent('INACTIVE')
            return True
        else:
            return False

    def identString(self):
        return self._id + " / " + self.ip_address + " (" + self.vendor + ")"

#    def __init__(self, mac_address):
#        self.mac_address = mac_address
#        self.ip_address = None
#        self.status = "ACTIVE"
#        self.first_seen = None
#        self.last_seen = None
#        self.ip_address_history = []
#        self.event_history = []

#    def printInfo(self):
#      print "IP: " + ip_address
#      print "MAC: " + mac_address
#      print ""

    def json(self):
      jsonData = {}
      jsonData['_id'] = self.mac_address
      jsonData['ip_address'] = self.ip_address
      jsonData['status'] = self.status
      jsonData['first_seen'] = self.first_seen
      jsonData['last_seen'] = self.last_seen
      return jsonData
