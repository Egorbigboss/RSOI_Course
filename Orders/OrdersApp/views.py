from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView, Response, Request
from OrdersApp.serializers import OrderSerializer
from OrdersApp.models import Order
from django.db.models import Q

# Create your views here.

class AllOrdersView(ListAPIView):

         def get(self, request: Request):
            if len(request.query_params) == 0:
            # Вообще все
                return Response(OrderSerializer(instance=Order.objects.all(), many=True).data)
        # Для определенного юзера
         try:
            user_id = request.query_params['user_id']
         except KeyError:
            return Response({'error': 'Wrong query params'}, status=status.HTTP_400_BAD_REQUEST)
         orders_amount = Order.objects.filter(Q(belongs_to_user_id = user_id))
         if len(orders_amount) == 0:
             return Response(status=status.HTTP_404_NOT_FOUND)
         serializer = OrderSerializer(instance=orders_amount, many=True)
         return Response(data=serializer.data, status=status.HTTP_200_OK)

class ConcreteOrderView(APIView):

    def get(self, request: Request, order_uuid):
         try:
             order = Order.objects.get(pk=order_uuid)
         except Order.DoesNotExist:
             return Response(status=status.HTTP_404_NOT_FOUND)
         serializer = orderSerializer(instance=orders_amount)
         return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: Request, order_uuid):
         try:
             order = Order.objects.get(pk=order_uuid)
         except Order.DoesNotExist:
             return Response(status=status.HTTP_404_NOT_FOUND)
         order.delete()
         return Response(status=status.HTTP_204_NO_CONTENT)
