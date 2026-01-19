from django.db import models

from user.models import User

from category.models import Category


# Create your models here.

class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    provider = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    average_duration = models.DurationField()



