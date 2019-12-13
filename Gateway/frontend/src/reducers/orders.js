import { GET_ORDERS } from '../components/orders/types';

const initialState = {
    orders: []
}

export default function ordersReducer(state = initialState, action) {
    switch (action.type) {
        case GET_ORDERS:
            console.log("REDUCER");
            return {
                ...state,
                orders: action.payload
            };
        default:
            return state;
    }
}


export const getOrdersState = state => state.orders;