from flask import Flask, jsonify, request
from api_utils import crossdomain
from datetime import datetime, timedelta
import couchdb

# Utilize replica for fast processing of views,
# but edits to the data must go to the master
master_couchdb_url = 'http://loyola.abarruda.com:5985/'
replica_couchdb_url = 'http://localhost:5984/'
trackerdb = 'test_tracker'

replica_couch = couchdb.Server(replica_couchdb_url)
replica_db = replica_couch[trackerdb]
master_couch = couchdb.Server(master_couchdb_url)
master_db = master_couch[trackerdb]


TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

app = Flask(__name__)

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
		event_time = datetime.strptime(formatted_timestamp, TIME_FORMAT)
		total_seconds = (datetime.now() - event_time).total_seconds()
		if (total_seconds <= threshold):
			results_in_range.append({'timestamp': timestamp, 'status': event_history[timestamp]})

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
