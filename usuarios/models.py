from django.db import models
from django.contrib.auth.models import AbstractUser

class Users(AbstractUser):
    
    rua = models.CharField(max_length=100, blank=True, null=True)
    numero = models.IntegerField(blank=True, null=True)
    cep = models.CharField(max_length=8, blank=True, null=True)