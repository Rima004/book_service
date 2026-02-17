from datetime import timedelta, date, datetime

from celery import shared_task
from .models import WorkSchedule,TimeSlot
from user.models import User

@shared_task
def generate_slots_for_provider(provider_id, schedule_id):
 provider = User.objects.get(id=provider_id)
 schedule = WorkSchedule.objects.get(id=schedule_id)

 SLOT_DURATION = timedelta(minutes=30)
 created_count =0
 day = date.today()

 start_dt = datetime.combine(day, schedule.start_time)
 end_dt = datetime.combine(day, schedule.end_time)

 current = start_dt

 while current + SLOT_DURATION <= end_dt:
  new_slot, created = TimeSlot.objects.get_or_create(
   provider=provider,
   date=day,
   start_time=current.time(),
   end_time=(current + SLOT_DURATION).time(),
   defaults={"is_available": True}
  )
  current += SLOT_DURATION
  if created:
   created_count += 1

 print(f"Создано слотов: {created_count}")




