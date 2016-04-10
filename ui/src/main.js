"use strict";
var React = require('react');
var ReactDOM = require('react-dom');
var HostList = require('./components/HostList.jsx');

//var baseUrl = "http://tracker-api.abarruda.com:10101";
var baseUrl = "http://loyola.abarruda.com:10101";
var POLL_INTERVAL = 30000;

var Enclosure = React.createClass({
	render: function() {
		return (
			<div className="container-fluid" ref="parentContainer">
				<div className="row">
					<div className="col-sm-4">
						<HostList title="Active Hosts" apiBaseUrl={baseUrl} dataSourceUrl={baseUrl + "/tracker/api/v1/active"} pollInterval={POLL_INTERVAL}/>
						<HostList title="Inactive Hosts" apiBaseUrl={baseUrl} dataSourceUrl={baseUrl + "/tracker/api/v1/inactive"} pollInterval={POLL_INTERVAL}/>
					</div>
				</div>
			</div>
		);
	}
});


ReactDOM.render(<Enclosure />, document.getElementById('app'));

module.exports = Enclosure;