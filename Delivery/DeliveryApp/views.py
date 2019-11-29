from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView, Response, Request
from DeliveryApp.serializers import DeliverySerializer
from DeliveryApp.models import DeliveryList
from django.db.models import Q
import datetime
from datetime import timedelta

date_format = "%Y-%m-%d"

class ConcreteUserDeliveryView(ListCreateAPIView):
    serializer_class = DeliverySerializer
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return DeliveryList.objects.filter(Q(user_id = user_id))

    def post(self,request : Request,user_id):
        delta = (datetime.datetime.strptime(str(datetime.datetime.now().date()), date_format) - datetime.datetime.strptime(str(request.data['date_of_creation'].split("T")[0]), date_format)).days
        if delta > int(request.data['days_for_clearing']):
            delivery_status = 'Ready for delivery'
        else:
            delivery_status = 'Not ready for delivery yet'
        serializer = DeliverySerializer(data = {
                'order_uuid' : request.data['order_uuid'],
                'user_id' : request.data['user_id'],
                'status' : delivery_status,
        })
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ConcreteDeliveryView(APIView):
    def get(self, request: Request, uuid):
         try:
             order = Delivery.objects.get(pk=uuid)
         except DeilveryList.DoesNotExist:
             return Response(status=status.HTTP_404_NOT_FOUND)
         serializer = DeliverySerializer(instance=order)
         return Response(data=serializer.data, status=status.HTTP_200_OK)


    def delete(self, request: Request, uuid):
         try:
             delivery = DeilveryList.objects.get(pk=uuid)
         except DeilveryList.DoesNotExist:
             return Response(status=status.HTTP_404_NOT_FOUND)
         delivery.delete()
         return Response(status=status.HTTP_204_NO_CONTENT)
