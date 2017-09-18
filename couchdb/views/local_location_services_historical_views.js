{
	"language": "javascript",
	"views": {
		"search_by_id_sort_by_timestamp": {
			"map": "function(doc) {\n  emit([doc.host_id, doc.timestamp], doc);\n}"
		}
	}
}
