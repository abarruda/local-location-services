import threading

class PeriodicTask(threading.Thread):
	def __init__(self):
		super(PeriodicTask, self).__init__()
		self.daemon = True

# Performs periodic compaction to keep database size down
class PeriodicCompaction (PeriodicTask):
	def __init__(self, interval, database):
		super(PeriodicCompaction, self).__init__()
		self.interval = interval
		self.database = database

	def run(self):
		print "Performing periodic compaction on database: " + str(self.database)
		self.database.compact()
		threading.Timer(self.interval, self.run).start()

# Performs periodic view call to keep current view up to date (and responses fast)
class PeriodicViewCall(PeriodicTask):
	def __init__(self, interval, database, viewName):
		super(PeriodicViewCall, self).__init__()
		self.interval = interval
		self.database = database
		self.viewName = viewName

	def run(self):
		print "Performing periodic view call (" + self.viewName + ") on database: " + str(self.database)
		self.database.view(self.viewName)