from django.shortcuts import render
from rest_framework import viewsets

from service.models import Service
from .permissions import CheckRole
from .serializers import ServiceSerializer


# Create your views here.



class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    permission_classes = [CheckRole]
    serializer_class =ServiceSerializer

    def perform_create(self, serializer):
        serializer.save(provider=self.request.user)


