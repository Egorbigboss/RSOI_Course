import React, { Component, Fragment } from 'react'
import { withAlert } from "react-alert";
import { connect } from 'react-redux';
import PropTypes from "prop-types";


export class Alerts extends Component {
    static propTypes = {
        error: PropTypes.object.isRequired,
        message: PropTypes.object.isRequired
    }

    componentDidUpdate(previousProps) {
        const { error, alert, message } = this.props;
        if (error !== previousProps.error) {
            if (error.msg.error) {
                alert.error(`Error: ${error.msg.error}`);
            }
        }

        if (message !== previousProps.message) {
            if (message.clothAdded) {
                alert.success(message.clothAdded)
            }
        }
        if (message !== previousProps.message) {
            if (message.clothDeleted) {
                alert.success(message.clothDeleted)
            }
        }
    }
    render() {
        return <Fragment />;
    }

}

const mapStateToProps = state => ({
    error: state.errors,
    message: state.messages
});


export default connect(mapStateToProps)(withAlert()(Alerts));
