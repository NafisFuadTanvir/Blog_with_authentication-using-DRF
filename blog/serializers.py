from rest_framework import serializers
from .models import Blog

class Blogserializer(serializers.ModelSerializer):
    class Meta:
        model=Blog
        fields=['id','title','content','slug','author','created_at','updated_At']
        read_only_fields=['author','created_at','updated_At']
        

class BlogCreateUpdateserializer(serializers.ModelSerializer):
    class Meta:
        model=Blog
        fields=['title','content']        