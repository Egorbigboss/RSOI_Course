from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView, Response, Request
from ClothsApp.serializers import ClothSerializer
from ClothsApp.models import Cloth
from rest_framework.generics import ListCreateAPIView
from django.db.models import Q

class AllClothsView(ListCreateAPIView):
    serializer_class = ClothSerializer
    def get_queryset(self):
        return Cloth.objects.all()

class StatsView(APIView):
    def get(self, request: Request):
        filter_type  = request.data['type_of_object']
        if filter_type is None:
            return Cloth.objects.all()
        count = Cloth.objects.filter(type_of_cloth = filter_type).count()
        content = {'count': count}
        return Response(content)

class ConcreteClothView(APIView):
    def get_object(self, pk):
        try:
            return Cloth.objects.get(pk=pk)
        except Cloth.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request: Request, cloth_uuid):
         try:
            cloth = Cloth.objects.get(pk=cloth_uuid)
         except Cloth.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
         serializer = ClothSerializer(instance=cloth)
         return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: Request, cloth_uuid):
         try:
             cloth = Cloth.objects.get(pk=cloth_uuid)
         except Cloth.DoesNotExist:
             return Response(status=status.HTTP_404_NOT_FOUND)
         cloth.delete()
         return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request: Request, cloth_uuid):
        try:
           cloth = Cloth.objects.get(pk=cloth_uuid)
        except Cloth.DoesNotExist:
           return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ClothSerializer(instance=cloth, data=request.data, partial=True) # set partial=True to update a data partially
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_NOT_FOUND)
