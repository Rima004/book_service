import re
from datetime import timedelta

from rest_framework import serializers


from service.models import Service


class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = "__all__"
        read_only_fields = ('created','provider')
