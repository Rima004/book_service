from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField




class User(AbstractUser):
 class Role(models.TextChoices):
  CLIENT = 'client', 'Client'
  PROVIDER = 'provider', 'Provider'

 first_name = models.CharField(max_length=100)
 last_name = models.CharField(max_length=100)
 email = models.EmailField(unique=True)
 password = models.CharField(max_length=128)
 role = models.CharField(choices=Role.choices, max_length=10, default=Role.CLIENT)
 phone_number = PhoneNumberField(region='MD')
 username = models.CharField(max_length=100, unique=True)
 image = models.ImageField(upload_to='images/',blank=True,null=True)


 REQUIRED_FIELDS = []
 USERNAME_FIELD = 'email'

def __str__(self):
    return self.email



