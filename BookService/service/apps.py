from django.apps import AppConfig
from django.core.signals import request_finished


class ServiceConfig(AppConfig):
   name = 'service'

   def ready(self):
       import service.signals