import sys
import os
import subprocess
from subprocess import CalledProcessError
from datetime import datetime
from libnmap.process import NmapProcess
from libnmap.parser import NmapParser
from Host import Host

class ScanUtils(object):

    # Scans for hosts in the specified network range using nmap.
    # Nmap does not to do a port scan after host discovery. This is often known as a "ping scan"
    # and is by default one step more intrusive than the list scan, and can often be used for 
    # the same purposes. It allows light reconnaissance of a target network without attracting much
    # attention.
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
            print("Nmap scan error: " + str(nm.stderr))

        scanTime = datetime.now() - scanStart
        print "Number of hosts detected: " + str(numHosts) + " (scan time: " + str(scanTime) + ")"
        return detectedHosts


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
                arpMac = subprocess.check_output("arp -a " + ip + " | awk '{print $4}'", shell=True)
                print "DEBUG: arpMac: '" + arpMac + "'" 
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