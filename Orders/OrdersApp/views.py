from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView, Response, Request
from OrdersApp.serializers import OrderSerializer
from OrdersApp.models import Order
from django.db.models import Q

# Create your views here.



class ConcreteUserOrdersView(APIView):
    def get(self,request : Request, user_id):
        request=self.request
        if user_id == None:
            return Response(OrderSerializer(instance=Order.objects.all(), many=True).data)
        orders_amount = Order.objects.filter(Q(belongs_to_user_id = user_id))
        if len(orders_amount) == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(instance=orders_amount, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request : Request,user_id):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AllOrdersView(APIView):
    def get(self,request : Request):
        request=self.request
        return Response(OrderSerializer(instance=Order.objects.all(), many=True).data)

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
