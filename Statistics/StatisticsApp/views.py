from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView, Response, Request
from StatisticsApp.serializers import StatsSerializer
from StatisticsApp.models import Stats
from django.db.models import Q
import json
import logging
logger = logging.getLogger("mylogger")




class CreateStatsView(ListCreateAPIView):
    serializer_class = StatsSerializer
    def get_queryset(self):
        return Stats.objects.all()


# class Update


class ConcreteStatsView(APIView):
    def get_object(self, pk):
        try:
            return Stats.objects.get(pk=pk)
        except Stats.DoesNotExist:
             return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request: Request, stats_uuid):
         try:
             stat = Stats.objects.get(pk=stats_uuid)
         except Stats.DoesNotExist:
             return Response(status=status.HTTP_404_NOT_FOUND)
         serializer = StatsSerializer(instance=stat)
         return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: Request, stats_uuid):
         try:
             stat = Stats.objects.get(pk=stats_uuid)
         except Stats.DoesNotExist:
             return Response(status=status.HTTP_404_NOT_FOUND)
         stat.delete()
         return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request: Request, stats_uuid):
        try:
            stat = Stats.objects.get(pk=stats_uuid)
        except Stats.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = StatsSerializer(instance=stat, data=request.data, partial=True) # set partial=True to update a data partially
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class UpdateStatsView(APIView):
    def patch(self, request: Request):
        object_type = request.data['filter']
        logger.info(object_type)
        create = Stats.objects.get_or_create(type_of_object = object_type)
        if object_type == 'dates':
            stat = Stats.objects.filter(type_of_object = object_type).update(text=request.data['days'])
        else:
            stat = Stats.objects.filter(type_of_object = object_type).update(count=request.data['count'])
        updated_stat = Stats.objects.get(type_of_object = object_type)
        serializer = StatsSerializer(instance=updated_stat)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
