import re
from contextlib import nullcontext
from datetime import timedelta
from math import ceil

from django.db.models.functions import NullIf
from rest_framework import serializers

from django.db import transaction
from service.models import Service

from service.models import WorkSchedule
from service.models import TimeSlot

from service.models import Booking


class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = "__all__"
        read_only_fields = ('created','provider')



class WorkScheduleSerializer(serializers.ModelSerializer):

    def validate(self, attrs):

       request = self.context["request"]
       qs =WorkSchedule.objects.filter(provider=request.user, workday=attrs.get('workday'))

       if self.instance:
           qs = qs.exclude(pk=self.instance.pk)

       if qs.exists():
           raise serializers.ValidationError(
               "This work day is already taken"
           )

       if attrs["end_time"] < attrs["start_time"]:
           raise serializers.ValidationError(
               "Время окончания не может быть меньше времени начала"
           )

       return attrs


    class Meta:
        model = WorkSchedule
        fields = ['workday', 'start_time', 'end_time', 'provider']
        read_only_fields = ('provider',)



class BookingCreateSerializer(serializers.ModelSerializer):
    id_slot = serializers.IntegerField(write_only=True)

    def validate_id_slot(self, value):
        if TimeSlot.objects.filter(id=value,is_available=True).exists():
            return value
        else:
            raise serializers.ValidationError("This slot is either  not available or does not exist")


    def create(self, validated_data):

        with transaction.atomic():

            id_slot = validated_data.pop("id_slot")
            service = validated_data["service"]

            # блокируем строки
            slot = TimeSlot.objects.select_for_update().get(id=id_slot)

            if not slot.is_available:
                raise serializers.ValidationError("This slot is not available")

            count_slots = ceil(service.average_duration.total_seconds() / 60 / 30 )

            slots = TimeSlot.objects.select_for_update().filter(
                provider=slot.provider,
                date=slot.date,
                start_time__gte=slot.start_time,
                is_available=True
            ).order_by("start_time")[:count_slots]

            if len(slots) != count_slots:
                raise serializers.ValidationError("Not enough consecutive available slots")

            for i in range(len(slots) - 1):
                if slots[i].end_time != slots[i + 1].start_time:
                    raise serializers.ValidationError("Slots are not consecutive")

            booking = Booking.objects.create(
                service=service,
                client=self.context["request"].user
            )


            TimeSlot.objects.filter(id__in=[s.id for s in slots]).update(
                booking=booking,
                is_available=False
            )

            return booking

    class Meta:
        model = Booking
        fields = ['service','id_slot']




class SlotsSerializer(serializers.ModelSerializer):
    class Meta:
        model=TimeSlot
        fields = "__all__"


class BookingPartialUpdateSerializer(serializers.ModelSerializer):


    def update(self, instance, validated_data):
        new_status = validated_data.pop("status")

        if new_status == Booking.Status.REJECTED:
            slots = TimeSlot.objects.filter(booking=instance)
            for slot in slots:
                slot.is_available = True
                slot.booking = None
                slot.save()
        elif new_status == instance.status:
            raise serializers.ValidationError("This status is already taken")

        instance.status = new_status
        instance.save()
        return instance


    class Meta:
        model =Booking
        fields = ['id','status']

        read_only_fields = ('id',)

class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = ['id','service','status','created']