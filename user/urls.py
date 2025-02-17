from django.contrib import admin
from django.urls import path,include
from .views import UserSignup, Userlogin,VerifyEmail,ResendverificationEmail

urlpatterns = [
    path('signup/',UserSignup.as_view(),name='signup'),
    path('verify-email/<str:token>/',VerifyEmail.as_view(),name='verify_email'),
    path('resend-verificationemail/',ResendverificationEmail.as_view(),name='resend-verificationemail'),
    path('login/',Userlogin.as_view(),name='login'),
    
    ]
    