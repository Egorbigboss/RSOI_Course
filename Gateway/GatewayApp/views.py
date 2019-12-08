from rest_framework.views import Response, Request, APIView
from GatewayApp.inter_service_requests import Requester


class CreateClothView(APIView):
    def post(self, request: Request):
        print(request.data)
        cloth_data = {"type_of_cloth", "days_for_clearing"}.intersection(
            request.data.keys()
        )
        if (
            (len(cloth_data)) != 2
            or (not request.data["type_of_cloth"])
            or (not request.data["days_for_clearing"])
        ):
            return Response(
                {"error": "Body must has type_of_cloth and days_for_clearing"},
                status=400,
            )
        response_json, code = Requester.create_cloth(
            type_of_cloth=request.data["type_of_cloth"],
            days_for_clearing=request.data["days_for_clearing"],
        )
        return Response(data=response_json, status=code)


class CreateOrderView(APIView):
    def post(self, request: Request):
        order_data = {"text", "type_of_cloth", "days_for_clearing"}.intersection(
            request.data.keys()
        )
        if (len(order_data)) != 3 or not request.user.is_authenticated:
            return Response(
                {
                    "error": "Body must have text and days_for_clearing and user must be autheicated "
                },
                status=400,
            )
        response_json, code = Requester.create_order(
            request,
            belongs_to_user_id=request.user.id,
            text=request.data["text"],
            type_of_cloth=request.data["type_of_cloth"],
            days_for_clearing=request.data["days_for_clearing"],
        )
        return Response(data=response_json, status=code)


class ClothsView(APIView):
    def get(self, request: Request):
        data, code = Requester.get_cloths(request)
        return Response(data, status=code)


class ConcreteClothView(APIView):
    def get(self, request: Request, cloth_uuid):
        data, code = Requester.get_concrete_cloth(str(cloth_uuid))
        return Response(data, status=code)

    def patch(self, request: Request, cloth_uuid):
        response_json, code = Requester.patch_concrete_cloth(
            cloth_uuid, data=request.data
        )
        return Response(data=response_json, status=code)

    def delete(self, request: Request, cloth_uuid):
        response_json, code = Requester.delete_concrete_cloth(
            request, cloth_uuid=cloth_uuid
        )
        return Response(data=response_json, status=code)


class ConcreteUserOrdersView(APIView):
    def get(self, request: Request, user_id):
        if int(user_id) == request.user.id:
            data, code = Requester.get_concrete_user_orders(request, user_id=user_id)
            return Response(data, status=code)
        return Response(
            {"error": "You can only check orders that belong to currently logged user"},
            status=400,
        )


class ConcreteUserDeliveryView(APIView):
    def get(self, request: Request, user_id):
        if int(user_id) == request.user.id:
            data, code = Requester.get_concrete_user_delivery(request, user_id=user_id)
            return Response(data, status=code)
        return Response(
            {
                "error": "You can only check delivery status that belong to currently logged user"
            },
            status=400,
        )


class CreateDeliveryList(APIView):
    def post(self, request: Request):
        if request.user.is_authenticated:
            data, code = Requester.create_delivery_list(
                request, user_id=request.user.id
            )
            return Response(data, status=code)
        return Response(
            {
                "error": "You can only init delivery list that belongs to currently logged user"
            },
            status=400,
        )


class OrdersView(APIView):
    def get(self, request: Request):
        data, code = Requester.get_orders(request=request)
        return Response(data, status=code)


class ConcreteOrderView(APIView):
    def get(self, request: Request, order_uuid):
        data, code = Requester.get_concrete_order(str(order_uuid))
        return Response(data, status=code)

    def patch(self, request: Request, order_uuid):
        response_json, code = Requester.patch_concrete_order(
            order_uuid, data=request.data
        )
        return Response(data=response_json, status=code)
