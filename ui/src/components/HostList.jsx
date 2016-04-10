"use strict";
var $ = require('jquery');
var React = require('react');
var Panel = require('react-bootstrap').Panel;
var Host = require('./Host.jsx');

var HostList = React.createClass({

    getInitialState: function() {
        return {
            data: []};
    },

    loadHostsFromServer: function() {
        $.ajax({
            url: this.props.dataSourceUrl,
            // The following is needed when talking directly to couchDB.
            // Allowing cross domain on the Flask side, so no longer needed
            //dataType: 'jsonp',
            cache: false,
            success: function(data) {
                var hostList = [];
                $(data.rows).each(function(index, obj) {
                    hostList.push({id: obj.id, name: obj.value.name, vendor: obj.value.vendor, status: obj.value.status, ip: obj.value.ip, firstSeen: obj.value.firstSeen, lastSeen: obj.value.lastSeen, lastEvent: obj.value.lastEvent});
                });
                this.setState({data: hostList});
            }.bind(this),
            error: function(xhr, status, err) {
                //console.error(this.props.dataSourceUrl, status, err.toString());
            }.bind(this)
        });
    },

    componentDidMount: function() {
        this.loadHostsFromServer();
        setInterval(this.loadHostsFromServer, this.props.pollInterval);
    },

    renderPanelTitle: function() {
        var count = $(this.state.data).length;
        return (
            <div>
                {this.props.title} <div className="badge">{count}</div>
            </div>
            );
    },

    render: function() {
    	var self = this;

        var count = $(this.state.data).length;

        var hosts = this.state.data.map(function(host) {
            var style = "primary";
            if (host.status === "INACTIVE") {
                style = "info";
            }
            return (
                <Host apiBaseUrl={self.props.apiBaseUrl} key={host.id} host={host} style={style}/>
                );
        });

        return (
            <div className="hostList">
                <Panel header={this.renderPanelTitle()}>
                        {hosts}
                    
                </Panel>
            </div>
            );
    }
});

module.exports = HostList;