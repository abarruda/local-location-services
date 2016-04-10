"use strict";
var React = require('react');
var Button = require('react-bootstrap').Button;
var Input = require('react-bootstrap').Input;
var Modal = require('react-bootstrap').Modal;

var UpdateHostModal = React.createClass({

    getInitialState: function() {
        return {nameValue: ''};
    },

    handleNameChange: function() {
        this.setState({nameValue: this.refs.hostNameInput.getValue()});
    },

    updateHost: function () {
        var apiUrl = this.props.apiBaseUrl + "/tracker/api/v1/" + this.props.host.id;

        $.ajax({
            url: apiUrl,
            cache: false,
            type: 'POST',
            data: {name: this.state.nameValue},
            success: function(data) {
                alert("The update was successful.  The data will refreshed shortly.");
                this.props.onClose();
            }.bind(this),
            error: function(xhr, status, err) {
                console.error(this.props.dataSourceUrl, status, err.toString());
                alert("UNABLE TO UPDATE!  Try again or check logs.");
            }.bind(this)
        });
    },

    render: function() {

        return (
            <Modal show={this.props.visible} onHide={this.props.onClose} container={this.refs.parentContainer} bsSize="small">
                <Modal.Header closeButton>
                    <Modal.Title>Modify {this.props.host.name}</Modal.Title>
                </Modal.Header>
                
                <Modal.Body>
                    <Input type="text"
                        label="Host's name:"
                        placeholder={this.props.host.name}
                        value={this.state.nameValue}
                        ref="hostNameInput"
                        onChange={this.handleNameChange} />
                </Modal.Body>

                <Modal.Footer>
                    <Button onClick={this.updateHost}>Save</Button>
                </Modal.Footer>
            </Modal>
        );

    }
});

module.exports = UpdateHostModal;