{
	"views": {
		"active_hosts": {
			"map": "function(doc)\n{\n  if (doc.status == 'ACTIVE') {\n    displayString = doc.vendor\n    if (doc.name != null) {\n      displayString = doc.name + \" - \" + displayString\n    }\n    emit(doc._id, displayString)\n  }\n}\n"
		},
		"first_seen_last_7_days": {
			"map": "function(doc)\n{\n  currentTime = new Date()\n  ageSinceSeen = currentTime - (new Date(doc.first_seen)).getTime()\n  if (ageSinceSeen < (7 * 24 * 60 * 60 * 1000)) {\n    displayString = doc.vendor\n    if (doc.name != null) {\n      displayString = displayString + \" - \" + doc.name\n    }\n    emit(doc._id, displayString)\n  }\n}\n"
		},
		"first_seen_last_day": {
			"map": "function(doc)\n{\n  currentTime = new Date()\n  ageSinceSeen = currentTime - (new Date(doc.first_seen)).getTime()\n  if (ageSinceSeen < (24 * 60 * 60 * 1000)) {\n    displayString = doc.vendor\n    if (doc.name != null) {\n      displayString = displayString + \" - \" + doc.name\n    }\n    emit(doc._id, displayString)\n  }\n}\n"
		},
		"unknown": {
			"map": "function(doc) {\n  if (doc.name == null || doc.name == \"Unknown\") {\n    emit(doc._id, {FirstSeen: doc.first_seen, LastSeen: doc.last_seen, Vendor: doc.vendor});\n  }\n}"
		},
		"api_active_hosts": {
			"map": "function(doc)\n{\n  if (doc.status == 'ACTIVE') {\n    nameDisplayString = \"Unknown\";\n    if (doc.name != null) {\n      nameDisplayString = doc.name;\n    }\n    emit(doc._id, {name:nameDisplayString, vendor: doc.vendor, status: doc.status, firstSeen: doc.first_seen, lastSeen: doc.last_seen, lastEvent: doc.last_event, ip: doc.ip_address});\n  }\n}\n"
		},
		"api_inactive_hosts": {
			"map": "function(doc)\n{\n  if (doc.status == 'INACTIVE') {\n    nameDisplayString = \"Unknown\";\n    if (doc.name != null) {\n      nameDisplayString = doc.name;\n    }\n    emit(doc._id, {name:nameDisplayString, vendor: doc.vendor, status: doc.status, firstSeen: doc.first_seen, lastSeen: doc.last_seen, lastEvent: doc.last_event, ip: doc.ip_address});\n  }\n}\n"
		}
	}
}
