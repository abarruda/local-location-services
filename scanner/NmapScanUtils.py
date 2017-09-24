from ScanUtils import ScanUtils

from libnmap.process import NmapProcess
from libnmap.parser import NmapParser
from Host import Host

class NmapScanUtils(ScanUtils):

    def __init__(self, config):
        self.networkRange = config.get('nmap', 'IP_SCAN_RANGE')

    # Scans for hosts in the specified network range using nmap.
    # Nmap does not to do a port scan after host discovery. This is often known as a "ping scan"
    # and is by default one step more intrusive than the list scan, and can often be used for 
    # the same purposes. It allows light reconnaissance of a target network without attracting much
    # attention.
    #@staticmethod
    def scanNetwork(self):
        print str(scanStart) + " - Scanning network for hosts..."

        nm = NmapProcess(targets=self.networkRange, options="-sP -n")
        nm.run()

        numHosts = 0
        detectedHosts = {}
        if nm.rc == 0:
            nmap_report = NmapParser.parse(nm.stdout)

            for host in nmap_report.hosts:
                if host.is_up():
                    detectedHost = Host(_id=host.mac, ip_address=host.ipv4, vendor=host.vendor)
                    detectedHosts[detectedHost._id] = detectedHost
                    numHosts += 1
        else:
            print("Nmap scan error: " + str(nm.stderr))

        return detectedHosts