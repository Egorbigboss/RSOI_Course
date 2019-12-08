import { GET_CLOTHS, DELETE_CLOTH, ADD_CLOTH } from "../actions/types.js"

const initialState = {
    gateways: []
};



export default function (state = initialState, action) {
    switch (action.type) {
        case GET_CLOTHS:
            return {
                ...state,
                gateways: action.payload
            }
        case DELETE_CLOTH:
            return {
                ...state,
                gateways: state.gateways.filter(cloth => cloth.uuid !== action.payload)
            }
        case ADD_CLOTH:
            return {
                ...state,
                gateways: [...state.gateways, action.payload]
            }
        default:
            return state;

    }
}