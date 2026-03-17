from django.shortcuts import render
from rest_framework import viewsets

from category.models import Category

from category.serializers import CategorySerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
