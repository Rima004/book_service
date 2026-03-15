from datetime import timedelta, date, datetime
from turtledemo.clock import current_day

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


@shared_task
def generate_weekly_slots():
    today = date.today()
    today_weekday = today.weekday()
    duration = timedelta(minutes=30)

    for schedule in WorkSchedule.objects.all():
        work_weekday = schedule.workday
        count_day = (work_weekday - today_weekday)%7
        slot_date = today + timedelta(days=count_day)

        start_dt = datetime.combine(slot_date, schedule.start_time)
        end_dt = datetime.combine(slot_date, schedule.end_time)
        current = start_dt
        while current + duration <= end_dt:
            slot_start = current
            slot_end = current + duration
            TimeSlot.objects.get_or_create(provider=schedule.provider,date=slot_date,start_time=slot_start.time(),end_time=slot_end.time())

            current+=duration









