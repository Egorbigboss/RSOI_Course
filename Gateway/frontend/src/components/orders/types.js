export const GET_ORDERS = 'GET_ORDERS';

export function getOrdersSucess(res) {
    console.log("tUT");
    return {
        type: GET_ORDERS,
        orders: res
    }
}
