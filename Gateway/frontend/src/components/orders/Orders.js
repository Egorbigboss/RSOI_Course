import React, { Component, Fragment } from 'react';
import { useAlert } from "react-alert";
import { Link } from 'react-router-dom'

const options = { year: 'numeric', month: 'numeric', day: 'numeric' };

const initialState = {
    deleteAlert: "",
}

function formatDate(string) {
    var options = { year: 'numeric', month: 'numeric', day: 'numeric' };
    return new Date(string).toLocaleDateString([], options);
}


function deleteOrder(uuid) {
    return fetch(`/api/orders/${uuid}`, {
        mode: 'cors', // no-cors, cors, *same-origin
        method: 'DELETE',
    })
    .then()
    .catch(error => {
        console.log("tut");
        console.log(error);
    })
}

export class Orders extends Component {
    constructor(props) {
        super(props);

        this.state = {
            orders: [],
        };
    }

    componentDidMount() {
        fetch('/api/orders/')
            .then((response) => response.json())
            .then(json =>
                this.setState({
                    orders: json
                })
            );
    }

    render() {

        const { orders } = this.state;
        console.log(orders)
        return (
            <Fragment>
                <div>
                    <h2>Orders
                        <table className="table table-striped">
                            <thead>
                                <tr>
                                    <th>UUID</th>
                                    <th>Type of cloth</th>
                                    <th>Date</th>
                                    <th />
                                </tr>
                            </thead>
                            <tbody>
                                {orders.map(order => (
                                    <tr key={order.uuid}>
                                        <td>{order.uuid}</td>
                                        <td>{order.type_of_cloth}</td>
                                        <td>{formatDate(order.date_of_creation)}</td>
                                        <td><button onClick={deleteOrder.bind(this, order.uuid)}
                                            className="btn btn-danger btn-sm">
                                            Delete</button>
                                        </td>
                                    </tr>

                                ))}
                            </tbody>
                        </table>
                    </h2>
                </div>
            </Fragment>
        );
    };

}

export default Orders;
