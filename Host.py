# Class represents an Host that has connected to
# the network that is being tracked

from datetime import datetime
from datetime import timedelta
from couchdb.mapping import Mapping, Document, TextField, DateTimeField, DictField

class Host(Document):
    _id = TextField()
    ip_address = TextField()
    vendor = TextField()
    name = TextField()
    status = TextField(default="ACTIVE")
    first_seen = DateTimeField(default=datetime.now)
    last_seen = DateTimeField(default=datetime.now)
    #last_event = DictField(Mapping.build(status = TextField(), timestamp = DateTimeField()), default={'',''})
    last_event = DictField(default={})
    ip_address_history = DictField()
    event_history = DictField()

    def update(self, ip_address, vendor):
      # There is a slight discrepency with storing the datetime this way
      # and using str(datetime.now())
      self.last_seen = datetime.now()
      self.ip_address = ip_address
      self.recordIp()

      if self.status == 'INACTIVE':
          self.activate()

    def activate(self):
        print self.identString() + " has become ACTIVE"
        self.status = 'ACTIVE'
	timestamp = datetime.now()
        self.event_history[str(timestamp)] = self.status
        self.recordLastEvent(self.status, str(timestamp))

    def inactivate(self):
        self.status = 'INACTIVE'
        self.event_history[str(self.last_seen)] = self.status
        self.recordLastEvent(self.status, self.last_seen)

    # The "last_event" field was added to the document structure after creation.
    # Ran into problems inserting records into the dictionary if it didn't already exist,
    # so I resorted to the code below to initialize the field and retain any data there 
    # from previous updates.  Surely, there is a better solution than this.
    def recordLastEvent(self, status, timestamp):
        last_event_dict = dict()
        last_event_dict.update({str(status): str(timestamp)})
        last_event_dict.update(self.last_event)
        self.last_event = last_event_dict

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
        if (self.name is None):
            displayName = "<Unknown>"
        else:
            displayName = self.name
        return self._id + " / " + self.ip_address + " (" + displayName + ", " + self.vendor + ")"

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
      jsonData['last_event'] = self.last_event
#      print "DEBUG: self.last_event: " + self.last_event
      return jsonData
