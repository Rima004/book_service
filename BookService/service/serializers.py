import re
from datetime import timedelta

from rest_framework import serializers


from service.models import Service


class ServiceSerializer(serializers.ModelSerializer):
    custom_duration = serializers.SerializerMethodField()

    def get_custom_duration(self, obj):
        total_seconds = int(obj.duration.total_seconds())
        hours = total_seconds // 3600
        minutes = round((total_seconds % 3600) / 60)
        if hours and minutes:
            return f'{hours}h and {minutes} min'
        elif hours:
            return f'{hours}h'
        return f'{minutes} min'


    def validate_duration(self, value):
        value= value.strip()
        pattern = r"^(?:[01]\d|2[0-3]):[0-5]\d$"
        if not re.match(pattern, value):
            raise serializers.ValidationError('Формат должен быть HH:MM')
        hours,minutes = map(int,value.split(':'))
        return timedelta(hours=hours, minutes=minutes)

    class Meta:
        model = Service
        fields = "__all__"
        read_only_fields = ('created','provider')
