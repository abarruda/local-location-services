import sys, os
from flask import Flask, jsonify, request
from api_utils import crossdomain
from datetime import datetime, timedelta
import couchdb
from periodic_tasks import PeriodicCompaction, PeriodicViewCall
import ConfigParser

if len(sys.argv) < 2:
  print "A property file must be specified to start API!"
  sys.exit(1)

configFile = sys.argv[1]
if not os.path.isfile(configFile):
  print "Property file does not exist, cannot start API!"
  sys.exit(1)

print "Using configuration file: " + configFile
config = ConfigParser.ConfigParser()
config.read(configFile)

# Utilize replica for fast processing of views,
# but edits to the data must go to the master
master_couchdb_host = os.getenv("COUCHDB_HOST", config.get('database', 'MASTER_DB_HOST'))
master_couchdb_port = os.getenv("COUCHDB_PORT", config.get('database', 'MASTER_DB_PORT'))
master_couchdb_url = "http://" + master_couchdb_host + ":" + master_couchdb_port
print "Connecting to master couchdb @ '" + master_couchdb_url + "'"
master_hosts_db = config.get('database', 'MASTER_DB_NAME')

replica_couchdb_host = os.getenv("COUCHDB_HOST", config.get('database', 'REPLICA_DB_HOST'))
replica_couchdb_port = os.getenv("COUCHDB_PORT", config.get('database', 'REPLICA_DB_PORT'))
replica_couchdb_url = "http://" + replica_couchdb_host + ":" + replica_couchdb_port
print "Connecting to replica couchdb @ '" + replica_couchdb_url + "'"
replica_db_name = config.get('database', 'REPLICA_DB_NAME')
historical_db_name = config.get('database', 'HISTORICAL_DB_NAME')

replica_couch = couchdb.Server(replica_couchdb_url)
replica_db = replica_couch[replica_db_name]
replica_historical_db = replica_couch[historical_db_name]
master_couch = couchdb.Server(master_couchdb_url)
master_db = master_couch[master_hosts_db]

TIME_FORMAT_V1 = '%Y-%m-%d %H:%M:%S'
TIME_FORMAT_V2 = '%Y-%m-%dT%H:%M:%SZ'
PRETTY_TIME_FORMAT = '%m/%d/%Y - %H:%M:%S'
COMPACTION_INTERVAL = 21600 #6 hours
VIEW_CALL_INTERVAL = 86400 #24 hours

app = Flask(__name__)
PeriodicCompaction(COMPACTION_INTERVAL, replica_db).start()
PeriodicCompaction(COMPACTION_INTERVAL, replica_historical_db).start()
PeriodicViewCall(VIEW_CALL_INTERVAL, replica_db, 'local_location_services/api_active_hosts').start()

@app.route('/')
def index():
	return "A-Net Tracker API"

@app.route('/hosts/api/v1/all', methods=['GET'])
def get_all():
	results = replica_db.view('_all_docs', include_docs=True)
	return results

@app.route('/hosts/api/v1/active', methods=['GET'])
@crossdomain(origin='*')
def get_active_hosts():
	view_results = replica_db.view('local_location_services/api_active_hosts', descending=True)
	return jsonify(rows = view_results.rows)

@app.route('/hosts/api/v1/inactive', methods=['GET'])
@crossdomain(origin='*')
def get_inactive_hosts():
	view_results = replica_db.view('local_location_services/api_inactive_hosts', descending=True)
	return jsonify(rows = view_results.rows)

@app.route('/hosts/api/v1/<id>/event-history/<int:hours>', methods=['GET'])
@crossdomain(origin='*')
def event_history(id, hours):
	threshold = hours * 60 * 60
	host = replica_db[id]
	event_history = host['event_history']
	results_in_range = []
	for timestamp in sorted(event_history):
		# some timestamps include a decimal in the seconds position.
		# strip that off to make time formatting easier
		formatted_timestamp = timestamp[0:timestamp.rfind('.')]
		event_time = datetime.strptime(formatted_timestamp, TIME_FORMAT_V1)
		total_seconds = (datetime.now() - event_time).total_seconds()
		if (total_seconds <= threshold):
			results_in_range.append({'timestamp': timestamp, 'status': event_history[timestamp]})

	return jsonify(rows = results_in_range)

@app.route('/hosts/api/v2/<id>/event-history/<int:hours>', methods=['GET'])
@crossdomain(origin='*')
def event_history_from_replica_database(id, hours):
	threshold = str(datetime.now() - timedelta(hours = hours))
	results_in_range = []
	view_results = replica_historical_db.view('local_location_services_historical/search_by_id_sort_by_timestamp', startkey=[id, threshold], endkey=[id, {}])
	for result in view_results:
		try:
			pretty_timestamp = datetime.strptime(result.value['timestamp'], TIME_FORMAT_V2).strftime(PRETTY_TIME_FORMAT)
			results_in_range.append({'timestamp': pretty_timestamp, 'status': result.value['status']})
		except:
			print "Unsupported timestamp format: " + result.value['timestamp']

	return jsonify(rows = results_in_range)

@app.route('/hosts/api/v1/<id>', methods=['POST'])
@crossdomain(origin='*')
def update(id):
	host = master_db[id]
	old_host_name = host['name']
	host['name'] = request.form['name'];
	master_db.save(host);
	print "Changed host (" + id + ") '" + old_host_name + "' to '" + request.form['name'] + "'" 
	return 'SUCCESS'

api_port = config.get('api', 'API_PORT')
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=api_port, debug=True)
