from django.shortcuts import render
from rest_framework import generics,status
from .serializers import UserSerializer
from .models import CustomUser
from rest_framework.response import Response


#the createapiview only deals with the post request
class UserSignup(generics.CreateAPIView):
    serializer_class= UserSerializer

#the Genericapiview can handle any request    
class VerifyEmail(generics.GenericAPIView):
    def get(self,request,token):
        user=CustomUser.objects.filter(verification_token=token).first()
        if user:
            if user.is_verified:
                return Response(
                    {"detail":"successfully verified"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user.is_verified=True
            user.verification_token=None
            user.save()
            return Response(
                {"details":"successfully verified"},
                status=status.HTTP_200_OK
            )
        return Response(
            {"details":"invalid token"},
            status=status.HTTP_400_BAD_REQUEST
        )    