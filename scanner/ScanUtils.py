import os
import subprocess
from subprocess import CalledProcessError
from datetime import datetime

class ScanUtils(object):

	def __init__(self, config):
		self.config = config

	# Performs an ICMP ping on the specified IP address.  If the ping is successful (0 return code),
	# the ARP table is checked to determine if the mac address that responded to the ping matches 
	# the specified mac address.  If so, the ping is considered successful, resulting in an active, 
	# known host.  The ARP table entry is cleared before the ping is attempted.
	@staticmethod
	def pingAndVerifyMacAddress(ip, mac):
		print "Verifying mac '" + mac + "' for IP address " + ip + "..."
		result = False
		message = ""

		pingStart = datetime.now()
		print "Deleting arp cache entry for " + ip
		os.system("arp -d " + ip)
		clearedArpEntry = subprocess.check_output("arp -a " + ip, shell=True)
		print clearedArpEntry

		# ping once, 1 second timeout, throw away output (only care about status code)
		response = os.system("ping -c 1 -w 1 " + ip + " > /dev/null")
		if response == 0:
			try:
				arpMac = subprocess.check_output("arp -a " + ip + " | awk '{print $4}'", shell=True).rstrip().upper()
				print "DEBUG: arpMac: '" + arpMac + "'" 
				if arpMac == mac:
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