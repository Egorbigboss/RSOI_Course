import axios from "axios";

import { GET_ORDERS } from "./types";

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
    console.log("Menya zvali");
};
