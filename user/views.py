from django.shortcuts import render
from django.urls import reverse
from rest_framework import generics,status
from .serializers import UserSerializer,UserUpdateSerializer
from .models import CustomUser
from rest_framework.response import Response
from django.utils.crypto import get_random_string
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

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
        
        
        
class ForgotPasswordView(generics.GenericAPIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response(
                {"detail": "Email is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = CustomUser.objects.filter(email=email).first()
        if not user:
            return Response(
                {"detail": "User with this email does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )

        
        user.reset_password_token = get_random_string(length=32)
        user.save()

        # Build the reset password link
        reset_link = request.build_absolute_uri(
            reverse(
                viewname='reset_password',
                kwargs={"token": user.reset_password_token}
            )
        )

        # Render the email template
        subject = "Reset Your Password"
        html_content = render_to_string('emails/reset_password_email.html', {
            "user": user.username,
            "reset_link": reset_link
        })

        # Send the email
        email = EmailMultiAlternatives(
            subject,
            "This is a text version of the email.",
            "from@example.com",
            [user.email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)

        return Response(
            {"detail": "Password reset email sent."},
            status=status.HTTP_200_OK
        )   
        
class ResetPasswordView(generics.GenericAPIView):
    def post(self, request, token):
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        if not new_password or not confirm_password:
            return Response(
                {"detail": "both new_password and confirm_password are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if new_password != confirm_password:
            return Response(
                {"detail": "Passwords didn't  match."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = CustomUser.objects.filter(reset_password_token=token).first()
        if not user:
            return Response(
                {"detail": "Invalid or expired token."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Update the password and clear the token
        user.set_password(new_password)
        user.reset_password_token = None
        user.save()

        return Response(
            {"detail": "Password has been reset successfully."},
            status=status.HTTP_200_OK
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
                
class RetriveUpdateProfile(generics.RetrieveUpdateAPIView):
    queryset=CustomUser.objects.all()
    permission_classes=[IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def get_serializer_class(self):
        if self.request.method in ['PUT','PATCH']:
            return UserUpdateSerializer
        return UserSerializer
                    