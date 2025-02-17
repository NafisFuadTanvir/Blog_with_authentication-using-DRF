from django.shortcuts import render
from django.urls import reverse
from rest_framework import generics,status
from .serializers import UserSerializer
from .models import CustomUser
from rest_framework.response import Response
from django.utils.crypto import get_random_string
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from rest_framework_simplejwt.tokens import RefreshToken
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
        
#in Genericapiview there is no need to add a serializer
class ResendverificationEmail(generics.GenericAPIView):
    def post(self,request):
        given_email=request.data.get('email')
        if not given_email:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user= CustomUser.objects.filter(email=given_email).first() 
        if not user:
            return Response(
                {
                    "details":"user with this email can't found"
                },status=status.HTTP_404_NOT_FOUND
            )
        if user.is_verified:
            return Response(
                {
                    "details":"email already verified"
                },status=status.HTTP_400_BAD_REQUEST
            )       
        user.verification_token=get_random_string(length=32)
        user.save()
        
        verification_link=self.request.build_absolute_uri(
                reverse(
                    viewname='verify_email',
                    kwargs={"token":user.verification_token}
                    
                )
            )    
        
        #render the email template
        subject="verify your email"
        html_content= render_to_string('emails/verification_email.html',{
                "user":user.username,
                "verification_link":verification_link
            })
            
        #create an email message
        email= EmailMultiAlternatives(
                subject,
                "this is a text version of the email",
                "from@example.com",
                [user.email]
                )
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)
        
        return Response(
            {
                "details":"verification email sent"
            },status=status.HTTP_200_OK
        )
        

class Userlogin(generics.GenericAPIView):
    def post(self,request):
        email= request.data.get('email')
        password= request.data.get('password')
        
        if not email or not password:
            return Response(
                {"details":"creadentials not valid"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        db_user= CustomUser.objects.filter(email=email).first()
        if not db_user:
            return Response(
                {"details":"creadentials not valid"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        matched_password= db_user.check_password(password)
        
        if not matched_password:
            return Response(
                {"details":"creadentials not valid"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        if not db_user.is_verified:
            return Response(
                {"details":"email is not yet verified"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        refresh= RefreshToken.for_user(db_user)
        
        return Response(
            {
                "refresh_token":str(refresh),
                "access_token":str(refresh.access_token)
            }
        )        
                
                