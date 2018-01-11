from ScanUtils import ScanUtils

from easysnmp import Session
from manuf import manuf
from Host import Host

class SnmpScanUtils(ScanUtils):

	def __init__(self, config):
		self.config = config
		self.oid = config.get('snmp', 'OID')
		self.host = config.get('snmp', 'HOST')
		# The following is necessary because the manuf project is currently broken.
		# It assumes that the manuf file uses a '#' preceeding the vendor comment
		# on each line.  However the file retrieved via the update does not preceed
		# each comment with the '#' character.  We are forced to use the manuf file
		# that comes with the project which is formatted in a way that can be parsed.  
		# (https://github.com/coolbho3k/manuf/blob/master/manuf/manuf.py#L88)
		self.macParser = manuf.MacParser('/scanner/src/manuf/manuf/manuf')

	def scanNetwork(self):
		
		session = Session(hostname=self.host, community='public', version=2)
		items = session.walk(self.oid)

		numHosts = 0
		detectedHosts = {}
		for item in items:
			ip = str.replace(str(item.oid), self.oid, '')
			mac = ':'.join([ '%0.2x' % ord(_) for _ in item.value ]).upper()
			vendor = self.macParser.get_comment(mac)
			if vendor is not None:
				vendorString = vendor
			else:
				vendorString = "<Unknown>"
			host = Host(_id=mac, ip_address=ip, vendor=vendorString)
			detectedHosts[host._id] = host
			numHosts += 1

		return detectedHosts
