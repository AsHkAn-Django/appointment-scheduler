from django.db import models
from django.conf import settings


MINUTES = [(m, m) for m in range(10, 60, 10)]
HOURS = [(h, h) for h in range(8, 17)]

class Appointment(models.Model):
    '''A model for taking appointment.'''
    date = models.DateField()
    hour = models.IntegerField(choices=HOURS, max_length=2)
    minute = models.IntegerField(choices=MINUTES, max_length=2)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='appointments', on_delete=models.CASCADE)
    details = models.TextField(blank=True, null=True)
    visited = models.BooleanField(default=False)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'date', 'hour', 'minute'], name='unique_appointment')]

    def __str__(self):
        return f"{self.user} on {self.date} at {self.get_time()}"

    def get_time(self):
        return f"{self.hour}:{self.minute}"