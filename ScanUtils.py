import sys
import os
import subprocess
from subprocess import CalledProcessError
from datetime import datetime
from libnmap.process import NmapProcess
from libnmap.parser import NmapParser
from Host import Host

class ScanUtils(object):

	@staticmethod	
	def scanNetwork(networkRange):
		scanStart = datetime.now()
		print str(scanStart) + " - Scanning network for hosts..."

		nm = NmapProcess(targets=networkRange, options="-sP -n")
		nm.run()

		numHosts = 0
		detectedHosts = {}
		if nm.rc == 0:
			nmap_report = NmapParser.parse(nm.stdout)

			for host in nmap_report.hosts:
				if host.is_up():
					seen = datetime.now()
					detectedHost = Host(_id=host.mac, ip_address=host.ipv4, vendor=host.vendor)
					detectedHosts[detectedHost._id] = detectedHost
					numHosts += 1
		else:
			print(nm.stderr)

		scanTime = datetime.now() - scanStart
		print "Number of hosts detected: " + str(numHosts) + " (scan time: " + str(scanTime) + ")"
		return detectedHosts


	@staticmethod
	def pingAnVerifyMacAddress(ip, mac):
		result = False
		message = ""

		pingStart = datetime.now()
		# ping once, 1 second timeout, throw away output (only care about status code)
		response = os.system("ping -c 1 -w 1 " + ip + " > /dev/null")
		if response == 0:
			try:
				arpMac = subprocess.check_output("arp -a " + ip + " | awk '{print $4}'", shell=True)
				if arpMac.rstrip().upper() == mac:
					result = True
					message = "pinged and mac address verified successfully."
				else:
					message = "could not verify mac address (" + mac + ") with " + ip + " ('" + arpMac + "')."
			except CalledProcessError as e:
				message = "cannot verify host's mac address."
		else:
			message = "cannot be pinged."
			
		pingTime = datetime.now() - pingStart
		return (result, message, pingTime)