import React, { Component, Fragment } from 'react';
import { Link } from 'react-router-dom'

const initialState = {
    deleteAlert: "",
}

function deleteDelivery(uuid) {
    return fetch(`/api/delivery/${uuid}`, {
        mode: 'cors', // no-cors, cors, *same-origin
        method: 'DELETE',
    })
    .then()
    .catch(error => {
        console.log("tut");
        console.log(error);
    })
}

export class Delivery extends Component {
    constructor(props) {
        super(props);

        this.state = {
            delivery: [],
        };
    }

    componentDidMount() {
        fetch('/api/delivery/user/2')
            .then((response) => response.json())
            .then(json =>
                this.setState({
                    delivery: json
                })
            );
    }

    render() {

        const { delivery } = this.state;
        console.log(delivery)
        return (
            <Fragment>
                <div>
                    <h2>Delivery list
                        <table className="table table-striped">
                            <thead>
                                <tr>
                                    <th>UUID</th>
                                    <th>Status</th>
                                    <th />
                                </tr>
                            </thead>
                            <tbody>
                                {delivery.map(delivery => (
                                    <tr key={delivery.delivery_uuid}>
                                        <td>{delivery.uuid}</td>
                                        <td>{delivery.status}</td>
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

export default Delivery;
