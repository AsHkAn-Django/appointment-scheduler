from django import forms
from .models import Appointment
from datetime import datetime
from django.core.exceptions import ValidationError



class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['date', 'hour', 'minute', 'details']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'id': 'id_date'}),
            'details': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set initial empty choices for minute
        self.fields['minute'].choices = []
        self.fields['minute'].widget.attrs['disabled'] = 'disabled'
