from django.db import models
from django.conf import settings
from datetime import datetime
from django.utils.text import slugify
# Create your models here.

class Blog(models.Model):
    title= models.CharField(max_length=255)
    content=models.TextField()
    slug= models.SlugField(unique=True,blank=True)
    author=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='blogs')
    created_at= models.DateTimeField(auto_now_add=True)
    updated_At=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug= f"{slugify(self.title)}_{hash(datetime.now)}"
        super().save(*args,**kwargs)    
    