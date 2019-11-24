from rest_framework.views import Response, Request, APIView
from GatewayApp.inter_service_requests import Requester



class CreateCloth(APIView):
    def post(self, request : Request):
        cloth_data = {'type_of_cloth', 'days_for_clearing'}.intersection(request.data.keys())
        if (len(cloth_data)) != 2:
            return Response ({'error': 'Body must have type_of_cloth and days_for_clearing'},status=400)
        response_json, code = Requester.create_cloth(type_of_cloth=request.data['type_of_cloth'], days_for_clearing=request.data['days_for_clearing'])
        return Response(data=response_json, status=code)

class CreateOrderView(APIView):
    def post(self, request : Request,user_id):
        print("User ID - ",user_id)
        order_data = {'text','type_of_cloth','days_for_clearing'}.intersection(request.data.keys())
        if (len(order_data)) != 3:
            return Response ({'error': 'Body must have text and days_for_clearing'},status=400)
        response_json, code = Requester.create_order(belongs_to_user_id=user_id, text=request.data['text'], type_of_cloth=request.data['type_of_cloth'], days_for_clearing=request.data['days_for_clearing'])
        return Response(data=response_json, status=code)

# class ClothsView(APIView):
#     def get(self, request: Request):
#         data, code = Requester.get_cloths()
#         return Response(data, status=code)

class ConcreteClothView(APIView):
    def get(self, request: Request, cloth_uuid):
        data, code = Requester.get_concrete_cloth(str(Cloth_uuid))
        return Response(data, status=code)

class ConcreteUserOrdersView(APIView):
    def get(self, request: Request, user_id):
        data, code = Requester.get_orders(user_id=user_id)
        return Response(data, status=code)


class OrdersView(APIView):
    def get(self, request: Request):
        data, code = Requester.get_orders()
        return Response(data, status=code)


class ConcreteOrderView(APIView):
    def get(self, request: Request, image_uuid):
        data, code = Requester.get_concrete_order(str(image_uuid))
        return Response(data, status=code)
