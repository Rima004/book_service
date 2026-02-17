from django.contrib.admin import action
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.response import Response

from service.models import Service
from  .filters import *
from .models import WorkSchedule, TimeSlot,Booking
from .permissions import *
from .serializers import ServiceSerializer, WorkScheduleSerializer, SlotsSerializer,BookingCreateSerializer,BookingPartialUpdateSerializer,BookingSerializer
from rest_framework.status import  HTTP_405_METHOD_NOT_ALLOWED
# Create your views here.



class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    permission_classes = [CheckRole]
    serializer_class =ServiceSerializer


    def perform_create(self, serializer):
        serializer.save(provider=self.request.user)



class WorkScheduleViewSet(viewsets.ModelViewSet):
     serializer_class =WorkScheduleSerializer
     permission_classes = [WorkSchedulePermission]
     lookup_field = 'workday'

     def get_queryset(self):


        return WorkSchedule.objects.filter(provider=self.request.user)


     def perform_create(self, serializer):
         serializer.save(provider=self.request.user)


class SlotsViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class =SlotsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ClientSlotsFilter

    def get_queryset(self):

        if getattr(self, 'swagger_fake_view', False):
            return TimeSlot.objects.none()

        user = self.request.user
        if user.role == 'client':
            return TimeSlot.objects.filter(is_available=True)
        elif user.role == 'provider':
            return TimeSlot.objects.filter(provider=self.request.user)
        return TimeSlot.objects.none()

    def get_filterset_class(self):
        if self.request.user.role == 'client':
            return ClientSlotsFilter
        elif self.request.user.role == 'provider':
            return ProviderSlotsFilter
        return None


class BookingSetViewSet(viewsets.ModelViewSet):
    permission_classes = [PermissionsForBooking,permissions.IsAuthenticated]


    def get_queryset(self):
        if self.request.user.role == 'client':
            return Booking.objects.filter(client=self.request.user)
        elif self.request.user.role == 'provider':
            return Booking.objects.filter(service__provider=self.request.user)
        return Booking.objects.none()


    def get_serializer_class(self):
        if self.action == 'create':
           return BookingCreateSerializer
        elif self.action == 'partial_update':
            return BookingPartialUpdateSerializer
        return BookingSerializer


