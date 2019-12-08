import { GET_CLOTHS, DELETE_CLOTH, ADD_CLOTH } from "../actions/types.js"

const initialState = {
    cloths: []
};



export default function (state = initialState, action) {
    switch (action.type) {
        case GET_CLOTHS:
            return {
                ...state,
                cloths: action.payload
            }
        case DELETE_CLOTH:
            return {
                ...state,
                cloths: state.cloths.filter(cloth => cloth.uuid !== action.payload)
            }
        case ADD_CLOTH:
            return {
                ...state,
                cloths: [...state.cloths, action.payload]
            }
        default:
            return state;

    }
}