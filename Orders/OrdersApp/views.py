from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView, Response, Request
from OrdersApp.serializers import OrderSerializer
from OrdersApp.models import Order
from django.db.models import Q
import datetime
import logging
logger = logging.getLogger("mylogger")

# Create your views here.



class ConcreteUserOrdersView(ListCreateAPIView):
    serializer_class = OrderSerializer
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Order.objects.filter(Q(belongs_to_user_id = user_id))

class AllOrdersView(ListCreateAPIView):
    serializer_class = OrderSerializer
    def get_queryset(self):
        return Order.objects.all()

class StatsView(APIView):
    def get(self, request: Request):
        # filter_type  = request.data['date_of_creation']
        # if filter_type is None:
        #     return Order.objects.all()
        dates = Order.objects.values_list('date_of_creation', flat = True)
        date_stats = {1: 0, 2: 0, 3 : 0, 4 : 0, 5 : 0}
        for date in dates:
            date_stats[int(date.weekday())] = date_stats[int(date.weekday())] + 1
        content = {'days' : date_stats}
        return Response(content)


class ConcreteOrderView(APIView):
    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
             return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request: Request, order_uuid):
         try:
             order = Order.objects.get(pk=order_uuid)
         except Order.DoesNotExist:
             return Response(status=status.HTTP_404_NOT_FOUND)
         serializer = OrderSerializer(instance=order)
         return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: Request, order_uuid):
         try:
             order = Order.objects.get(pk=order_uuid)
         except Order.DoesNotExist:
             return Response(status=status.HTTP_404_NOT_FOUND)
         order.delete()
         return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request: Request, order_uuid):
        try:
            order = Order.objects.get(pk=order_uuid)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(instance=order, data=request.data, partial=True) # set partial=True to update a data partially
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)



