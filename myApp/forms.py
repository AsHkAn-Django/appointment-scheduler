# from django import forms
# from .models import Appointment
# from datetime import datetime
# from django.core.exceptions import ValidationError


# class AppointmentForm(forms.ModelForm):
#     # Overriding date and time fields in the Model by adding some widget to them
#     date = forms.DateField(
#         widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
#     )
#     time = forms.TimeField(
#         widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'})
#     )

#     class Meta:
#         model = Appointment
#         fields = ('date', 'time', 'details')


#     # Use clean method if you want to check multiple things
#     # But be sure always do these two things
#     # 1) Call parent at the beginning : cleaned_data = super().clean()
#     # 2) Return the clean data at the end : return cleaned_data
#     def clean(self):
#         '''Raise an error if the user chooses past days.'''

#         # Call the clean() parent to run the default validations and fill cleaned_data
#         cleaned_data = super().clean()

#         selected_date = self.cleaned_data.get('date')
#         selected_time = self.cleaned_data.get('time')

#         if selected_date and selected_time:
#             selected_datetime = datetime.combine(selected_date, selected_time)
#             if selected_datetime < datetime.now():
#                 raise ValidationError('The selected date and time must be in the future.')

#         return cleaned_data


#     # You can use an specific field with this structure clean_<fieldname>
#     # But remember
#     # 1) you can only work on one specific field here
#     # 2) return that field at the end
#     def clean_time(self):
#         '''Raise an error if the user chooses out of work schedule.'''
#         selected_time = self.cleaned_data.get('time')

#         if selected_time is None:
#             raise ValidationError('Invalid time selection.')
#         if not (8 <= selected_time.hour < 17):
#             raise ValidationError('The selected Time should be between 8AM - 5PM.')

#         return selected_time