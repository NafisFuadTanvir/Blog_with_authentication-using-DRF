from django.contrib import admin
from django.urls import path,include
from .views import UserSignup,VerifyEmail

urlpatterns = [
    path('signup/',UserSignup.as_view(),name='signup'),
    path('verify-email/<str:token>/',VerifyEmail.as_view(),name='verify_email')
    
    ]
    