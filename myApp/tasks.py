from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from myApp.models import Appointment


@shared_task
def send_reminder_email(user_email):
    '''Send user an email one day before their appointment'''
    subject = f"Just a reminder"
    message = f"Tomorrow you will have an appointment. Don't forget it!"
    send_mail(subject=subject,
              message=message,
              from_email=None,
              recipient_list=[user_email])


@shared_task
def check_tomorrow_appointments():
    '''Check all the appointments for tomorrow and send them reminder email.'''
    tomorrow_date = datetime.now().date() + timedelta(days=1)

    tomorrow_apps = Appointment.objects.filter(date=tomorrow_date)
    for app in tomorrow_apps:
        send_reminder_email.delay(app.user.email)

