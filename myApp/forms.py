from django import forms
from .models import Appointment, MINUTES, HOURS

class AppointmentForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'class': 'datepicker form-control','type': 'text'}))
    hour = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class': 'form-control'}))
    minute = forms.IntegerField(widget=forms.HiddenInput(), required=True)

    class Meta:
        model = Appointment
        fields = ['date', 'hour', 'minute', 'details']
        widgets = {'details': forms.Textarea(attrs={'class': 'form-control'}),}

    def __init__(self, *args, **kwargs):
        # Extract 'user' from kwargs for later validation in clean()
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Build dropdown options: list of tuples (value, display)
        allowed_hours = [(h, f"{h:02d}") for h, _ in HOURS]
        # Prepend an empty choice to prompt selection
        self.fields['hour'].choices = [('', 'Select hour')] + allowed_hours

    def clean_hour(self):
        # Retrieve raw input from cleaned_data
        hour = self.cleaned_data.get('hour')
        try:
            # Convert string choice to integer
            hour = int(hour)
        except (TypeError, ValueError):
            # Invalid if conversion fails
            raise forms.ValidationError("Invalid hour selected.")

        # Validate against allowed hours defined in model
        allowed_hours = [h for h, _ in HOURS]
        if hour not in allowed_hours:
            raise forms.ValidationError("Invalid hour selected.")
        return hour

    def clean_minute(self):
        # Ensure minute is one of the allowed slots
        minute = self.cleaned_data.get('minute')
        allowed_minutes = [m for m, _ in MINUTES]
        if minute not in allowed_minutes:
            raise forms.ValidationError("Invalid minute selected.")
        return minute

    def clean(self):
        # Form-level validation: check for duplicate appointment
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        hour = cleaned_data.get('hour')
        minute = cleaned_data.get('minute')

        # Proceed only if 'user' and all fields are present
        if self.user and date is not None and hour is not None and minute is not None:
            exists = Appointment.objects.filter(user=self.user, date=date, hour=hour, minute=minute, visited=False).exists()
            if exists:
                # Raise a non-field error to inform the user
                raise forms.ValidationError("You already have an ongoing appointment at this time.")
        return cleaned_data
