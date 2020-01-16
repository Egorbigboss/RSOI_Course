from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.views import Request, Response, APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.authtoken.models import Token
from oauth2_provider.contrib.rest_framework.permissions import IsAuthenticatedOrTokenHasScope, IsAuthenticated
from AuthApp.serializers import UserSerializer
from django.contrib.auth.models import User
import json

class CheckToken(APIView):
    # permission_classes = (IsAuthenticated, )
    permission_classes = (IsAuthenticatedOrTokenHasScope, )
    required_scopes = ('read', 'write')
    
    def get(self, request: Request, *args, **kwargs):
        print(request.data, request.headers)
        serializer = UserSerializer(instance=request.user)
        return Response(serializer.data, status = status.HTTP_200_OK)

class RegisterView(APIView):
    def post(self, request: Request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class LoginOAuth2(View):
    def get(self, request):
        return render(request, template_name='AuthApp/logIn.html')

    def post(self, request: HttpRequest):
        try:
            username = request.POST['username']
            password = request.POST['password']
        except KeyError:
            return HttpResponseBadRequest(json.dumps({'error': 'wrong form data'}))
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is None:
            return redirect(request.get_raw_uri())
        login(request, user)
        print(f'http://{request.get_host()}{request.GET["next"]}')
        ret = redirect(f'http://{request.get_host()}{request.GET["next"]}')
        # ret = redirect(f'http://127.0.0.1:8000/api/oauth/redirect/')
        # ret = redirect(f'http://127.0.0.1:8004/o/authorize/?client_id=1YXUKptOmANO2evy9b43XlaGPkJXROQqSdaP9CVN&grant_type=authorizacode&response_type=token')
        print("Redirect tut")
        print(ret)
        return ret