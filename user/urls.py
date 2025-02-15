from django.contrib import admin
from django.urls import path,include
from .views import UserSignup

urlpatterns = [
    path('signup/',UserSignup.as_view(),name="signup"),
    
    ]
    