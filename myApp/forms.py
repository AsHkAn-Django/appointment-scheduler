from django import forms
from .models import Appointment
from datetime import datetime
from django.core.exceptions import ValidationError


class AppointmentForm(forms.ModelForm):
    minute = forms.ChoiceField()
    class Meta:
        model = Appointment
        fields = ['date', 'hour', 'minute', 'details']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'datepicker', 'type': 'text'}),
        }

