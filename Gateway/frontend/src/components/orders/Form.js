import React, { Component } from 'react';

const initialState = {
    type_of_cloth: '',
    days_for_clearing: '',
    typeError: '',
    daysError: '',
    text: '',
}

export class Form extends Component {
    state = initialState;


    onChange = e => this.setState({ [e.target.name]: e.target.value });

    onSubmit = e => {
        e.preventDefault();
        const { type_of_cloth, days_for_clearing, text} = this.state;
        const cloth = { type_of_cloth, days_for_clearing, text };
        const isValid = this.validate();
        console.log(this.state)
        if (isValid) {
            console.log(this.state.days_for_clearing, this.state.type_of_cloth);
            fetch("/api/orders/",
            {
                method: "POST",
                mode: 'cors', // no-cors, cors, *same-origin
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
            },
            body: JSON.stringify({text: this.state.text, days_for_clearing: this.state.days_for_clearing, type_of_cloth: this.state.type_of_cloth})
        });
            this.setState(initialState)
        }
    };

    validate = () => {

        let typeError = "";
        let daysError = "";
        let textError = "";

        if (!this.state.type_of_cloth) {
            typeError = "Invalid type of cloth";
        }
        if (!this.state.text) {
            textError = "Invalid text";
        }
        if (!this.state.days_for_clearing) {
            daysError = "Invalid days for clearing";
        }
        if (this.state.days_for_clearing == "0") {
            daysError = "Invalid days for clearing";
        }

        if (typeError || daysError || textError) {
            this.setState({ typeError, daysError, textError })
            return false;
        }
        return true;
    }

    render() {
        const { type_of_cloth, days_for_clearing, text} = this.state;
        return (
            <div className="card card-body mt-4 mb-4">
                <h2>Add Order</h2>
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
                    <div style={{ fontSize: 12, color: "red" }}>{this.state.textError}</div>
                    <div className="form-group">
                        <label>Text</label>
                        <input
                            className="form-control"
                            type="text"
                            name="text"
                            onChange={this.onChange}
                            value={text}
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



export default Form;
