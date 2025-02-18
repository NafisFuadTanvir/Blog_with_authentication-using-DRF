from django.contrib import admin
from django.urls import path,include
from .views import ForgotPasswordView, ResetPasswordView, UserSignup, Userlogin,VerifyEmail,ResendverificationEmail,RetriveUpdateProfile
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
    path('signup/',UserSignup.as_view(),name='signup'),
    path('verify-email/<str:token>/',VerifyEmail.as_view(),name='verify_email'),
    path('resend-verificationemail/',ResendverificationEmail.as_view(),name='resend-verificationemail'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/<token>/', ResetPasswordView.as_view(), name='reset_password'),
    path('login/',Userlogin.as_view(),name='login'),
    path('profile/',RetriveUpdateProfile.as_view(),name='profile'),
    path('refresh/',TokenRefreshView.as_view(),name='refresh')
    
    ]
    