from django.db.models.expressions import result
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import  WorkSchedule,Booking,TimeSlot
from .tasks import generate_slots_for_provider
from django.core.mail import send_mail
from django.core.cache import cache

@receiver(post_save, sender=WorkSchedule)
def create_slots (sender, instance, created, **kwargs):
    key = f"schedule_{instance.provider.id}"
    cache.delete(key)
    if created:
        generate_slots_for_provider.delay(instance.provider.id, instance.id)

      



@receiver(post_save, sender=Booking)
def sen_email(sender, instance, created, **kwargs):
    if created:
        send_mail("New order",f" {instance.client.first_name} has ordered your service is called {instance.service.title}.","pervncukarina@gmail.com",[instance.service.provider.email])
    else:
        send_mail(
            subject="Booking status updated",
            message=f"The status of your booking is now: {instance.get_status_display()}",
            from_email="pervucnukarina@gmail.com",
            recipient_list=[instance.client.email],
        )
@receiver(post_save,sender=TimeSlot)
def update_cache(sender,instance,created,**kwargs):
    if not created:
        cache_key = f"slots_{instance.provider.id}"
        cache.delete(cache_key)
        cache.delete("slots_clients")








