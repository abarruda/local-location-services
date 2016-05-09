import threading

class PeriodicCompaction (threading.Thread):

	def __init__(self, database, interval):
		super(PeriodicCompaction, self).__init__()
		self.database = database
		self.interval = interval
		self.daemon = True
		

	def run(self):
		print "Performing periodic compaction on database: " + str(self.database)
		self.database.compact()
		threading.Timer(self.interval, self.run).start()
