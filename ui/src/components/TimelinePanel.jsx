"use strict";
var React = require('react');
var Panel = require('react-bootstrap').Panel;

var TimelinePanel = React.createClass({
    // getInitialState: function() {
    //     return {
    //         timeline: []
    //     };
    // },

    render: function() {

        var timelineDisplay = this.props.timeline.map(function(timeline) {
            var statusLabelClassName = "label";
            var statusGlyphClassName = "glyphicon";

            if (timeline.status === "ACTIVE") {
                statusLabelClassName += " label-primary";
                statusGlyphClassName += " glyphicon-chevron-right";
            } else {
                statusLabelClassName += " label-info";
                statusGlyphClassName += " glyphicon-chevron-left";
            }

            return (
                    <div key={timeline.timestamp}>
                        <div className={statusGlyphClassName}></div>
                        <div className="glyphicon glyphicon-user" />
                        <div className={statusLabelClassName}>{timeline.status}</div>
                        <div className="label label-default">{timeline.timestamp}</div>
                        <br /><br />
                    </div>
                );
        });

        return (
            <Panel collapsible expanded={this.props.expanded}>
                {timelineDisplay}
            </Panel>
            );
    }
});

module.exports = TimelinePanel;