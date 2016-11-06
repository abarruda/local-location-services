# Class representing an Event that is detected by the tracker

from couchdb.mapping import Mapping, Document, TextField, DateTimeField

class Event(Document):
	host_id = TextField()
	timestamp = DateTimeField()
	status = TextField()