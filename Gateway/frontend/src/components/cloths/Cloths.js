import React, { Component, Fragment } from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import { getCloths, deleteCloth } from '../../actions/cloths';

export class Cloths extends Component {
    static propTypes = {
        cloths: PropTypes.array.isRequired,
        getCloths: PropTypes.func.isRequired,
        deleteCloth: PropTypes.func.isRequired
    };

    componentDidMount() {
        this.props.getCloths();
    }

    render() {
        return (
            <Fragment>
                <div>
                    <h2>Cloths
                        <table className="table table-striped">
                            <thead>
                                <tr>
                                    <th>UUID</th>
                                    <th>Type of cloth</th>
                                    <th>Days for clearing</th>
                                    <th />
                                </tr>
                            </thead>
                            <tbody>
                                {this.props.cloths.map(cloth => (
                                    <tr key={cloth.uuid}>
                                        <td>{cloth.uuid}</td>
                                        <td>{cloth.type_of_cloth}</td>
                                        <td>{cloth.days_for_clearing}</td>
                                        <td><button onClick={this.props.deleteCloth.bind(this, cloth.uuid)}
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
    }
}

const mapStateToProps = state => ({
    cloths: state.cloths.cloths
})


export default connect(mapStateToProps, { getCloths, deleteCloth })
    (Cloths);
