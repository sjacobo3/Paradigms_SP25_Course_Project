from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=200, unique=True)
    email = models.EmailField(max_length=200, unique=True)
    password = models.TextField()