from django.db import models

from user.models import User

from category.models import Category


# Create your models here.
class WorkingDays(models.IntegerChoices):
    MONDAY = 0, "Понедельник"
    TUESDAY = 1, "Вторник"
    WEDNESDAY = 2, "Среда"
    THURSDAY = 3, "Четверг"
    FRIDAY = 4, "Пятница"
    SATURDAY = 5, "Суббота"
    SUNDAY = 6, "Воскресенье"


class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    provider = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    average_duration = models.DurationField(null=True)


class Booking (models.Model):
    class Status(models.IntegerChoices):
        PENDING = 1,'принятый'
        REJECTED = 2,'откланен'
        COMPLETED = 3,'завершен'

    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.IntegerField(choices=Status.choices,default=Status.PENDING)
    created = models.DateTimeField(auto_now_add=True)

class WorkSchedule(models.Model):


    provider = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="work_schedules"
    )

    workday = models.IntegerField(
        choices=WorkingDays.choices
    )

    start_time = models.TimeField()
    end_time = models.TimeField()


class TimeSlot(models.Model):
    provider = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    booking = models.ForeignKey(Booking, null=True,blank=True, on_delete=models.SET_NULL,)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    class Meta:
        constraints = [ models.UniqueConstraint(
            fields=['provider','date','start_time'],
            name="unique_provider_date_start"
        )]