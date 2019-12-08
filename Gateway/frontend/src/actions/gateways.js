import axios from "axios";
import { createMessage } from "./messages";

import { GET_CLOTHS, DELETE_CLOTH, ADD_CLOTH, GET_ORDERS, GET_ERRORS } from "./types";

//GET_CLOTHS
export const getCloths = () => dispatch => {
    axios
        .get("/api/cloths/")
        .then(res => {
            dispatch({
                type: GET_CLOTHS,
                payload: res.data
            });
        })
        .catch(err => console.log(err));
};


//DELETE_CLOTH
export const deleteCloth = (uuid) => dispatch => {
    axios
        .delete(`/api/cloths/${uuid}/`)
        .then(res => {
            dispatch(createMessage({ clothDeleted: 'Cloth was succesfully deleted!' }));
            dispatch({
                type: DELETE_CLOTH,
                payload: uuid
            });
        })
        .catch(err => console.log(err));
};

//ADD_CLOTH
export const addCloth = cloth => dispatch => {
    axios
        .post("/api/cloths/create/", cloth)
        .then(res => {
            dispatch(createMessage({ clothAdded: 'Cloth was succesfully added!' }));
            dispatch({
                type: ADD_CLOTH,
                payload: res.data
            })
        })
        .catch(err => {
            const errors = {
                msg: err.response.data,
                status: err.response.status
            }
            dispatch({
                type: GET_ERRORS,
                payload: errors
            })
        });

};

//GET_ORDERS
export const getOrders = () => dispatch => {
    axios
        .get("/api/orders/")
        .then(res => {
            dispatch({
                type: GET_ORDERS,
                payload: res.data
            });
        })
        .catch(err => console.log(err));
};