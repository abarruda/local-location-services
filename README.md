local-location-services
=======================
Network presence service

### Kubernetes Helm Install
A few values are required to deploy successfully:
- scanner.container.snmpHost
- ui.container.externalIp

Example: 
	
	cd helm-chart/local-location-services
	
	helm install --set scanner.container.snmpHost=10.0.0.1 --set ui.container.externalIp=10.10.10.1 .