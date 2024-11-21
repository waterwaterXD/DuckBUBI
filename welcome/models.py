from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
# Create your models here.

class Account(models.Model):
    userID = models.OneToOneField(User,on_delete=models.CASCADE , primary_key=True)
    u_name = models.CharField(max_length=20, blank=True, null=True)
    phone_number = models.IntegerField(blank=True, null=True)
    email = models.EmailField(max_length=300, blank=True, null=True)
    position = models.CharField(max_length=50, )
    company = models.CharField(max_length=50,)
