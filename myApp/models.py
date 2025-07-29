from django.db import models
from django.conf import settings



class Appointment(models.Model):
    '''A model for taking appointment.'''

    class Status(models.TextChoices):
        '''A class for setting the user appointment status.'''

        PENDING = 'pending', 'Pending'
        CONFIRMED = 'confirmed', 'Confirmed'
        CANCELED = 'canceled', 'Canceled'

    date = models.DateField()
    time = models.TimeField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='appointments', on_delete=models.CASCADE)
    details = models.TextField(blank=True, null=True)
    status = models.CharField(choices=Status.choices, max_length=10, default=Status.PENDING)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'date', 'time'], name='unique_appointment')]

    def __str__(self):
        return f"{self.user.username} on {self.date} at {self.time}"

