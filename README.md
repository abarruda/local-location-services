local-location-services
=======================
Network presence service

### Kubernetes Helm Install
A few values are required to deploy successfully:
- scanner.container.snmpHost
- couchdb.volume.server
- couchdb.volume.serverUser
- couchdb.volume.serverPassword
- ui.container.externalIp

Example: 
	
	cd helm-chart/local-location-services
	
	helm install --set scanner.container.snmpHost=10.0.0.1 --set couchdb.volume.server=10.0.0.2 --set couchdb.volume.serverUser=storageuser --set couchdb.volume.serverPassword=storagepassword --set ui.container.externalIp=10.10.10.1 .