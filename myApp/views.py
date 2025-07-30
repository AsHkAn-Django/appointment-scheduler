from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views import generic
from .models import Appointment
from .forms import AppointmentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


class IndexView(generic.TemplateView):
    template_name = "myApp/index.html"


class AppointmentFormView(LoginRequiredMixin, generic.CreateView):
    model = Appointment
    template_name = "myApp/appointment_form.html"
    form_class = AppointmentForm
    success_url = reverse_lazy('myApp:home')

    def form_valid(self, form):
        # Check if there is already an appointment at the same date and time for the user
        if Appointment.objects.filter(user=self.request.user, date=form.cleaned_data['date'], time=form.cleaned_data['time']).exists():
            messages.warning(self.request, 'You have already had an appointment at that date and time!')
            return redirect('myApp:home')

        # If no conflict, save the appointment and show a success message
        form.instance.user = self.request.user
        messages.success(self.request, 'Your appointment has been reserved.')
        return super().form_valid(form)



class AppointmentListView(generic.ListView):
    model = Appointment
    template_name = "myApp/appointment_list.html"
    context_object_name = 'appointments'

    def get_queryset(self):
        return Appointment.objects.filter(user=self.request.user)
