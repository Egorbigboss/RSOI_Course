import { combineReducers } from 'redux';
import gateways from './gateways'
import errors from "./errors";
import messages from "./messages";

export default combineReducers({
    gateways,
    errors,
    messages
});