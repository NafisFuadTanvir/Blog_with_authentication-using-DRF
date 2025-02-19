from django.contrib import admin
from django.urls import path,include
from .views import Bloglistview,Myblogs,Blogcreateview,Blogdetailsview,Blogupdateview,Blogdeleteview
urlpatterns = [
    path('',Bloglistview.as_view(),name='Blog-list'),
    path('myblogs/',Myblogs.as_view(),name='my-blogs'),
    path('create/',Blogcreateview.as_view(),name='create-blog'),
    path('<int:id>/',Blogdetailsview.as_view(),name='blog-details'),
    path('delete/<int:id>/',Blogdeleteview.as_view(),name='delete-view'),
    path('update/<int:id>/',Blogupdateview.as_view(),name='update-view')
     ]
    