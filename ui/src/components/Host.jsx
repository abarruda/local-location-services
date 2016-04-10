"use strict";
var $ = require('jquery');
var React = require('react');
var Button = require('react-bootstrap').Button;
var Panel = require('react-bootstrap').Panel;
var UpdateHostModal = require('./UpdateHostModal.jsx');
var TimelinePanel = require('./TimelinePanel.jsx');


var Host = React.createClass({
    getInitialState: function() {
        return {
            open: false,
            timelineExpanded: false,
            updateModalVisible: false,
            timeline: []};
    },

    loadTimelineFromServer: function() {
        var apiUrl = this.props.apiBaseUrl + "/tracker/api/v2/" + this.props.host.id + "/event-history/36";
        
        $.ajax({
            url: apiUrl,
            cache: false,
            success: function(data) {
                var timeline = [];
                $(data.rows).each(function(index, obj) {
                    console.log(obj);
                    timeline.push({timestamp: obj.timestamp, status: obj.status});
                });
                this.setState({timeline: timeline});
            }.bind(this),
            error: function(xhr, status, err) {
                console.error(this.props.dataSourceUrl, status, err.toString());
            }.bind(this)
        });
    },

    handleClick: function() {
        this.setState({ open: !this.state.open });
    },

    handleTimelineClick: function() {
        if (this.state.timelineExpanded === false) {
            // This means we're switch from a closed state to an open state,
            // so let's load the timeline data from the server
            this.loadTimelineFromServer();
        }
        this.setState({timelineExpanded: !this.state.timelineExpanded});
    },

    handleUpdateModalClick: function() {
        this.setState({updateModalVisible: !this.state.updateModalVisible});
    },

    handleUpdateModalClose: function() {
        this.setState({updateModalVisible: false});
    },

    render: function() {
        var noLastEvent = (typeof this.props.host.lastEvent === "undefined");

        var lastEvent;
        if (!noLastEvent) {
            if (typeof this.props.host.lastEvent.status === "undefined") {
                lastEvent = "N/A";
            } else {
                lastEvent = "Became " + this.props.host.lastEvent.status + " at " + this.props.host.lastEvent.timestamp;
            }
            
        }
        return (
            <div className="modal-container">
                <UpdateHostModal
                    visible={this.state.updateModalVisible} 
                    onClose={this.handleUpdateModalClose} 
                    host={this.props.host}
                    apiBaseUrl={this.props.apiBaseUrl}/>
                <Panel header={this.props.host.name} collapsible bsStyle={this.props.style}>
                    {lastEvent}<br />
                    <br />
                    Vendor: {this.props.host.vendor}<br />
                    IP Address: {this.props.host.ip}<br />
                    First Seen: {this.props.host.firstSeen}<br />
                    Last Seen: {this.props.host.lastSeen}<br />
                    <br />
                    Actions: <br />
                    <Button bsStyle="link" onClick={this.handleUpdateModalClick}>Edit Host</Button><br />
                    <Button bsStyle="link" onClick={this.handleTimelineClick}>Show Timeline</Button><small>(past 36 hours)</small>
                    <TimelinePanel key={this.props.host.id} expanded={this.state.timelineExpanded} 
                        host={this.props.host} timeline={this.state.timeline} />
                </Panel>
            </div>);
    }
});

module.exports = Host;