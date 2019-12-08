import React, { Component } from 'react';
import { connect } from "react-redux";
import PropTypes from 'prop-types';
import { addCloth } from "../../actions/cloths";


const initialState = {
    uuid: '',
    type_of_cloth: '',
    days_for_clearing: '',
    typeError: '',
    daysError: '',
}

export class Form extends Component {
    state = initialState;


    static propTypes = {
        addCloth: PropTypes.func.isRequired
    };

    onChange = e => this.setState({ [e.target.name]: e.target.value });

    onSubmit = e => {
        e.preventDefault();
        const { type_of_cloth, days_for_clearing } = this.state;
        const cloth = { type_of_cloth, days_for_clearing };
        const isValid = this.validate();
        if (isValid) {
            console.log(this.state);
            this.props.addCloth(cloth);
            this.setState(initialState)
        }
        // this.setState(initialState)
    };

    validate = () => {

        let typeError = "";
        let daysError = "";

        if (!this.state.type_of_cloth) {
            typeError = "Invalid type of cloth";
        }
        if (!this.state.days_for_clearing) {
            daysError = "Invalid days for clearing";
        }
        if (this.state.days_for_clearing == "0") {
            daysError = "Invalid days for clearing";
        }

        if (typeError || daysError) {
            this.setState({ typeError, daysError })
            return false;
        }
        return true;
    }

    render() {
        const { type_of_cloth, days_for_clearing } = this.state;
        return (
            <div className="card card-body mt-4 mb-4">
                <h2>Add Cloth</h2>
                <form onSubmit={this.onSubmit}>
                    <div className="form-group">
                        <label>Type of cloth</label>
                        <input
                            className="form-control"
                            type="text"
                            name="type_of_cloth"
                            onChange={this.onChange}
                            value={type_of_cloth}
                        />
                    </div>
                    <div style={{ fontSize: 12, color: "red" }}>{this.state.typeError}</div>
                    <div className="form-group">
                        <label>Days for clearing</label>
                        <input
                            className="form-control"
                            type="int"
                            name="days_for_clearing"
                            onChange={this.onChange}
                            value={days_for_clearing}
                        />
                    </div>
                    <div style={{ fontSize: 12, color: "red" }}>{this.state.daysError}</div>
                    <div className="form-group">
                        <button type="submit" className="btn btn-primary">
                            Submit
                      </button>
                    </div>
                </form>
            </div>
        );
    }
}



export default connect(null, { addCloth })(Form);
