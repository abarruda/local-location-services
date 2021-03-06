# Class represents a Host that has connected to
# the network that is being tracked

from datetime import datetime
from datetime import timedelta
from couchdb.mapping import Mapping, Document, TextField, DateTimeField, DictField

class Host(Document):

    STATUS_ACTIVE = 'ACTIVE'
    STATUS_INACTIVE = 'INACTIVE'

    _id = TextField()
    ip_address = TextField()
    vendor = TextField()
    name = TextField()
    status = TextField(default="ACTIVE")
    first_seen = DateTimeField()
    last_seen = DateTimeField()
    #last_event = DictField(Mapping.build(status = TextField(), timestamp = DateTimeField()), default={'',''})
    last_event = DictField(default={})
    ip_address_history = DictField()
    event_history = DictField()

    def update(self, timestamp, ip_address, vendor):
      # There is a slight discrepency with storing the datetime this way
      # and using str(datetime.now())
      self.last_seen = timestamp
      self.ip_address = ip_address
      self.recordIp()

      if self.isInactive():
          self.activate(timestamp)

    # Marks a host as ACTIVE and records the event.
    def activate(self, timestamp):
        print self.identString() + " has become ACTIVE"
        self.status = self.STATUS_ACTIVE
        self.recordLastEvent(self.status, str(timestamp))

    # Marks a host as INACTIVE and records the event
    def inactivate(self):
        self.status = self.STATUS_INACTIVE
        self.recordLastEvent(self.status, self.last_seen)

    # Records an event
    def recordLastEvent(self, status, timestamp):
        self.last_event = {'status': status, 'timestamp': str(timestamp)}

    # Increments and records the IP address count in the host record
    def recordIp(self):
        if self.ip_address in self.ip_address_history:
            currentValue = self.ip_address_history[str(self.ip_address)]
            self.ip_address_history[str(self.ip_address)] = currentValue + 1
        else:
            self.ip_address_history[str(self.ip_address)] = 1

    def isActive(self):
      return self.status == self.STATUS_ACTIVE

    def isInactive(self):
      return self.status == self.STATUS_INACTIVE

    # Determines if the host has not been seen for greater than the specified 
    # amount of minutes.
    @staticmethod
    def isIdleFor(host, timestamp, minutes):
      if (timestamp - host.last_seen).total_seconds() > (minutes * 60):
        return True
      return False

    def isInactiveWithIdleTime(self, timestamp, minutes):
        # if host is past the idle threshold, mark INACTIVE
        idleTimeSeconds = (timestamp-self.last_seen).total_seconds()
        if (self.isActive() and self.isIdleFor(self, timestamp, minutes)):
            idleMinutes, idleSeconds = divmod(idleTimeSeconds, 60)
            print(self.identString() + " has gone INACTIVE (" + \
                 str(idleMinutes) + " minutes, " + \
                 str(idleSeconds) + " seconds)")
            return True
        else:
            return False

    def identString(self):
        if (self.name is None):
            displayName = "<Unknown>"
        else:
            displayName = self.name
        return self._id + " / " + self.ip_address + " (" + displayName + ", " + self.vendor + ")"

    def json(self):
      jsonData = {}
      jsonData['_id'] = self.mac_address
      jsonData['ip_address'] = self.ip_address
      jsonData['status'] = self.status
      jsonData['first_seen'] = self.first_seen
      jsonData['last_seen'] = self.last_seen
      jsonData['last_event'] = self.last_event
      return jsonData
