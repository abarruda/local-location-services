from flask import Flask, jsonify, request
from api_utils import crossdomain
from datetime import datetime, timedelta
import couchdb
from periodic_tasks import PeriodicCompaction, PeriodicViewCall

# Utilize replica for fast processing of views,
# but edits to the data must go to the master
master_couchdb_url = 'http://loyola.abarruda.com:5985/'
replica_couchdb_url = 'http://localhost:5984/'
master_tracker_db = 'test_tracker'
master_replica_db = 'tracker'
tracker_historical_db = 'tracker_historical'

replica_couch = couchdb.Server(replica_couchdb_url)
replica_db = replica_couch[master_replica_db]
replica_historical_db = replica_couch[tracker_historical_db]
master_couch = couchdb.Server(master_couchdb_url)
master_db = master_couch[master_tracker_db]

TIME_FORMAT_V1 = '%Y-%m-%d %H:%M:%S'
TIME_FORMAT_V2 = '%Y-%m-%dT%H:%M:%SZ'
PRETTY_TIME_FORMAT = '%m/%d/%Y - %H:%M:%S'
COMPACTION_INTERVAL = 21600 #6 hours
VIEW_CALL_INTERVAL = 86400 #24 hours

app = Flask(__name__)
PeriodicCompaction(COMPACTION_INTERVAL, replica_db).start()
PeriodicCompaction(COMPACTION_INTERVAL, replica_historical_db).start()
PeriodicViewCall(VIEW_CALL_INTERVAL, replica_db, 'tracker/api_active_hosts').start()

@app.route('/')
def index():
	return "A-Net Tracker API"

@app.route('/tracker/api/v1/all', methods=['GET'])
def get_all():
	results = replica_db.view('_all_docs', include_docs=True)
	return results

@app.route('/tracker/api/v1/active', methods=['GET'])
@crossdomain(origin='*')
def get_active_hosts():
	view_results = replica_db.view('tracker/api_active_hosts')
	return jsonify(rows = view_results.rows)

@app.route('/tracker/api/v1/inactive', methods=['GET'])
@crossdomain(origin='*')
def get_inactive_hosts():
	view_results = replica_db.view('tracker/api_inactive_hosts')
	return jsonify(rows = view_results.rows)

@app.route('/tracker/api/v1/<id>/event-history/<int:hours>', methods=['GET'])
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

@app.route('/tracker/api/v2/<id>/event-history/<int:hours>', methods=['GET'])
@crossdomain(origin='*')
def event_history_from_tracker_historical_db(id, hours):
	threshold = str(datetime.now() - timedelta(hours = hours))
	results_in_range = []
	view_results = replica_historical_db.view('tracker/search_by_id_sort_by_timestamp', startkey=[id, threshold], endkey=[id, {}])
	for result in view_results:
		pretty_timestamp = datetime.strptime(result.value['timestamp'], TIME_FORMAT_V2).strftime(PRETTY_TIME_FORMAT)
		results_in_range.append({'timestamp': pretty_timestamp, 'status': result.value['status']})

	return jsonify(rows = results_in_range)

@app.route('/tracker/api/v1/<id>', methods=['POST'])
@crossdomain(origin='*')
def update(id):
	host = master_db[id]
	old_host_name = host['name']
	host['name'] = request.form['name'];
	master_db.save(host);
	print "Changed host (" + id + ") '" + old_host_name + "' to '" + request.form['name'] + "'" 
	return 'SUCCESS'

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=10101, debug=True)
