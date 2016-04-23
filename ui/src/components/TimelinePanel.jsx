"use strict";
var React = require('react');
var Panel = require('react-bootstrap').Panel;

var TimelinePanel = React.createClass({

    render: function() {

    	var timelineDisplay = function(timeline) {
    		if (timeline.length === 0) {
    			return (<div>No recent activity.</div>);	
    		} else {
    			return (
    				timeline.map(function(event) {
    					var statusLabelClassName = "label";
    					var statusGlyphClassName = "glyphicon";

	    				if (event.status === "ACTIVE") {
	    					statusLabelClassName += " label-primary";
	    					statusGlyphClassName += " glyphicon-chevron-right";
	    				} else {
	    					statusLabelClassName += " label-info";
	    					statusGlyphClassName += " glyphicon-chevron-left";
	    				}

	    				return (
	    					<div key={event.timestamp}>
	    						<div className={statusGlyphClassName}></div>
	    						<div className="glyphicon glyphicon-user" />
	    						<div className={statusLabelClassName}>{event.status}</div>
	    						<div className="label label-default">{event.timestamp}</div>
	    						<br /><br />
							</div>
						);
	    			})
	    		);
    		}
    		
    	};

        return (
            <Panel collapsible expanded={this.props.expanded}>
                {timelineDisplay(this.props.timeline)}
            </Panel>
            );
    }
});

module.exports = TimelinePanel;