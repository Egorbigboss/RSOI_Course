from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView, Response, Request
from ClothsApp.serializers import ClothSerializer
from ClothsApp.models import Cloth
from rest_framework.generics import ListCreateAPIView

class AllClothsView(ListCreateAPIView):
    serializer_class = ClothSerializer
    def get_queryset(self):
        return Cloth.objects.all()


class ConcreteClothView(APIView):
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

# class AddClothToClothView(APIView)
