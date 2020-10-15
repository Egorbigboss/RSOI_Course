from rest_framework.views import Response, Request, APIView
from GatewayApp.inter_service_requests import Requester
from django.shortcuts import redirect
from django.views import View


class CreateClothView(APIView):
    def post(self, request : Request):
        cloth_data = {'type_of_cloth', 'days_for_clearing'}.intersection(request.data.keys())
        if (len(cloth_data)) != 2:
            return Response ({'error': 'Body must have type_of_cloth and days_for_clearing'},status=400)
        response_json, code = Requester.create_cloth(type_of_cloth=request.data['type_of_cloth'], days_for_clearing=request.data['days_for_clearing'])
        return Response(data=response_json, status=code)

class CreateOrderView(APIView):
    def post(self, request : Request):
        order_data = {'text','type_of_cloth','days_for_clearing'}.intersection(request.data.keys())
        if ((len(order_data)) != 3  or not Requester.check_token(request)):
            return Response ({'error': 'Body must have text and days_for_clearing and user must be autheicated '},status=400)
        user_json, user_code = Requester.get_user(request)
        user_id = user_json['id']
        response_json, code = Requester.create_order(request, belongs_to_user_id=request.user.id, text=request.data['text'], type_of_cloth=request.data['type_of_cloth'], days_for_clearing=request.data['days_for_clearing'])
        return Response(data=response_json, status=code)

class ClothsView(APIView):
    def get(self, request: Request):
        data, code = Requester.get_cloths(request)
        return Response(data, status=code)

class ConcreteClothView(APIView):
    def get(self, request: Request, cloth_uuid):
        data, code = Requester.get_concrete_cloth(str(cloth_uuid))
        return Response(data, status=code)

    def patch(self, request : Request, cloth_uuid):
        response_json, code = Requester.patch_concrete_cloth(cloth_uuid, data=request.data)
        return Response(data=response_json, status=code)

class ConcreteUserOrdersView(APIView):
    def get(self, request: Request):
        if Requester.check_token(request):
            user_json, user_code = Requester.get_user(request)
            user_id = user_json['id']
            print(user_id)
            data, code = Requester.get_concrete_user_orders(request,user_id=user_id)
            return Response(data, status=code)
        return Response ({'error': 'You can only check orders that belong to currently logged user'},status=400)

class ConcreteUserDeliveryView(APIView):
    def get(self, request: Request):
        if Requester.check_token(request):
            user_json, user_code = Requester.get_user(request)
            user_id = user_json['id']
            data, code = Requester.get_concrete_user_delivery(request,user_id=user_id)
            return Response(data, status=code)
        return Response ({'error': 'You can only check delivery status that belong to currently logged user'},status=400)

class CreateDeliveryList(APIView):
    def post(self, request: Request):
        if Requester.check_token(request):
            user_json, user_code = Requester.get_user(request)
            user_id = user_json['id']
            data, code = Requester.create_delivery_list(request,user_id=request.user.id)
            return Response(data, status=code)
        return Response ({'error': 'You can only init delivery list that belongs to currently logged user'},status=400)

class OrdersView(APIView):
    def get(self, request: Request):
        data, code = Requester.get_orders(request=request)
        return Response(data, status=code)

class ConcreteOrderView(APIView):
    def get(self, request: Request, order_uuid):
        data, code = Requester.get_concrete_order(str(order_uuid))
        return Response(data, status=code)

    def patch(self, request : Request, order_uuid):
        response_json, code = Requester.patch_concrete_order(order_uuid, data=request.data)
        return Response(data=response_json, status=code)

class StatsView(APIView):
    def get(self, request: Request):
        data, code = Requester.collect_stats(request=request)
        return Response(data, status=code)
    
    def post(self, request : Request):
        stat_data = {'type_of_object', 'text'}.intersection(request.data.keys())
        if (len(stat_data)) != 2:
            return Response ({'error': 'Body must have type_of_object and text'},status=400)
        response_json, code = Requester.create_metric(type_of_object=request.data['type_of_object'], text=request.data['text'])
        return Response(data=response_json, status=code)

class MetricsView(APIView):
    def get(self, request: Request):
        data,code = Requester.update_metric(request, data = request.data)
        return Response(data=data, status=code)

class ConcreteStatView(APIView):
    def get(self, request: Request, stat_uuid):
        data, code = Requester.get_concrete_metric(str(stat_uuid))

class ConcreteOrderView(APIView):
    def get(self, request: Request, order_uuid):
        data, code = Requester.get_concrete_order(str(order_uuid))
        return Response(data, status=code)

    def patch(self, request : Request, order_uuid):
        response_json, code = Requester.patch_concrete_order(order_uuid, data=request.data)
        return Response(data=response_json, status=code)

class AuthenicateUser(APIView):
    def post(self, request: Request):
        data, code = Requester.authenticate_user(request,data=request.data)
        return Response(data,code)

class GetUser(APIView):
    def get(self, request: Request):
        data, code = Requester.get_user(request)
        return Response(data,code)


class OLoginView(View):
    def get(self, request):
        uri = 'http://127.0.0.1:8004/o/authorize/?client_id=1YXUKptOmANO2evy9b43XlaGPkJXROQqSdaP9CVN&grant_type=authorization_code&response_type=code&redirect_uri=http%3A%2F%2F127.0.0.1:8000%2Fapi%2Foauth%2Fredirect%2F'
        return redirect(uri)

class ORedirectView(APIView):
    def get(self, request: Request):
        import requests
        print(request.query_params)
        code = request.query_params['code']
        data_to_send = f'client_id=1YXUKptOmANO2evy9b43XlaGPkJXROQqSdaP9CVN&client_secret=hl4rcSjqgssnzok1VTnEm5U00Zcc7Ov43oqPjRVjBdZidk4HWnHltsSHRve6UvFWMQQhzNwQQ8X5BvczKPdt8nAdQQdujLO9TV5Dy7tEfpuK0OMPEG8n8QLzAnHokkcI&code={code}&grant_type=authorization_code'
        ret = requests.post(url='http://127.0.0.1:8004/o/token/', data=data_to_send,
                            headers={'content-type': 'application/x-www-form-urlencoded'})
        print("RET",ret)
        return Response(ret.json(), status=ret.status_code)
