from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):
    is_verified= models.BooleanField(default=False)
    verification_token= models.CharField(max_length=50,blank=True,null=True)
    bio=models.TextField(blank=True)
    image=models.ImageField(upload_to='profile_images/',blank=True,null=True)
    
    
    