import React, { Component, Fragment } from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import { getOrders } from '../../actions/orders';

export class Orders extends Component {
    // static propTypes = {
    //     orders: PropTypes.array.isRequired,
    //     getOrders: PropTypes.func.isRequired,
    // };


    ComponentDidMount() {
        this.props.getOrders();
    }

    render() {
        return (
            <div>
                <h1>Orders List</h1>
            </div>
        );
    }
}

const mapStateToProps = state => ({
    orders: state.orders.orders
})

export default connect(mapStateToProps, { getOrders })(Orders);
