from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

ROLE_CH0ICES = [
    ('client','Client'),
    ('provider','Provider'),
]



class User(AbstractUser):

 first_name = models.CharField(max_length=100)
 last_name = models.CharField(max_length=100)
 email = models.EmailField(unique=True)
 password = models.CharField(max_length=128)
 role = models.CharField(choices=ROLE_CH0ICES, max_length=10, default='client')
 phone_number = models.CharField(max_length=11)
 username = models.CharField(max_length=100, unique=False)


 USERNAME_FIELD = 'email'


