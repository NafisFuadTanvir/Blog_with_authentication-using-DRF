from django.shortcuts import render
from rest_framework import generics,status
from .serializers import UserSerializer
from .models import CustomUser
from rest_framework.response import Response


#the createapiview only deals with the post request
class UserSignup(generics.CreateAPIView):
    serializer_class= UserSerializer
    
    