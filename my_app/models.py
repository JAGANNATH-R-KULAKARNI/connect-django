import pickletools
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Person(models.Model):
    added_by=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=20,primary_key=True)
    bio=models.CharField(max_length=60)
    age=models.IntegerField()
    gender=models.CharField(max_length=10)
    pic=models.CharField(max_length=1000,default='')
    
    def __str__(self):
        return '@'+self.name
    
    

class Posts(models.Model):
    person_name=models.ForeignKey(Person,on_delete=models.CASCADE)
    text=models.CharField(max_length=1000)
    media_link=models.CharField(max_length=200)
    time_posted=models.CharField(max_length=100)
    likes=models.IntegerField()
    comments=models.JSONField()
    
    
        
    