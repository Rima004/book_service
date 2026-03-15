from django_filters import rest_framework as filters

from .models import TimeSlot


class ClientSlotsFilter(filters.FilterSet):

   start_time = filters.TimeFilter(field_name='start_time', lookup_expr='gte')
   provider = filters.NumberFilter(field_name='provider__id')

   class Meta:
        model = TimeSlot
        fields = ['provider','start_time']

class ProviderSlotsFilter(filters.FilterSet):
    start_time = filters.TimeFilter(field_name='start_time', lookup_expr='gte')
    end_time = filters.TimeFilter(field_name='end_time', lookup_expr='lte')

    class Meta:
        model = TimeSlot
        fields = ['start_time', 'end_time']