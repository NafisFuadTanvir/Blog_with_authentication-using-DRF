from rest_framework import generics,permissions
from .models import Blog
from .serializers import Blogserializer,BlogCreateUpdateserializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.http import Http404

# creating pagination class
class Blogpagination(PageNumberPagination):
    page_size=5
    page_size_query_param='page_size'
    max_page_size=10

#blog listing view    
class Bloglistview(generics.ListAPIView):
    queryset= Blog.objects.all().order_by('-created_at') 
    serializer_class= Blogserializer
    pagination_class=Blogpagination  
 
#personal blog listing view
class Myblogs(generics.ListAPIView):
    serializer_class=Blogserializer
    permission_classes=[IsAuthenticated]
    pagination_class=Blogpagination
    
    def get_queryset(self):
        return Blog.objects.filter(author=self.request.user)
       

#single blog detail_view
class Blogdetailsview(generics.RetrieveAPIView):
    queryset=Blog.objects.all()
    serializer_class=Blogserializer
    lookup_field='id'

#blog create view
class Blogcreateview(generics.CreateAPIView):
    serializer_class= BlogCreateUpdateserializer
    permission_classes=[IsAuthenticated] 
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

#blog update view
class Blogupdateview(generics.UpdateAPIView):
    queryset=Blog.objects.all()
    serializer_class= BlogCreateUpdateserializer
    permission_classes= [IsAuthenticated]
    lookup_field='id'
    
    def get_object(self):
        blog=super().get_object()
        if blog.author != self.request.user:
            raise Http404
        return blog  

#blog delete views
class Blogdeleteview(generics.DestroyAPIView):
    queryset=Blog.objects.all()
    permission_classes= [IsAuthenticated]
    lookup_field='id'
    
    def get_object(self):
        blog=super().get_object()
        if blog.author != self.request.user:
            raise Http404
        return blog  
                   