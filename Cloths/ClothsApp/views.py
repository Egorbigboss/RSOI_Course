from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView, Response, Request
from ClothsApp.serializers import ClothSerializer
from ClothsApp.models import Cloth
from django.db.models import Q

# Create your views here.

class AllClothsView(APIView):
    def get(self, request: Request):
        return Response(ClothSerializer(instance=Cloth.objects.all(), many=True).data)
        # try:
        #     user_id = request.query_params['user_id']
        # except KeyError:
        #     return Response({'error': 'Wrong query params'}, status=status.HTTP_400_BAD_REQUEST)
        # cloths_amount = Cloth.objects.filter(Q(belongs_to_user_id = user_id))
        # if len(cloths_amount) == 0:
        #     return Response(status=status.HTTP_404_NOT_FOUND)
        # serializer = ClothSerializer(instance=cloths_amount, many=True)
        # return Response(data=serializer.data, status=status.HTTP_200_OK)

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
