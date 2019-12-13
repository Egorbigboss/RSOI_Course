import { combineReducers } from 'redux';
import cloths from "./cloths";
import errors from "./errors";
import messages from "./messages";
import orders from "./orders";

export default combineReducers({
    cloths,
    orders,
    errors,
    messages,
});