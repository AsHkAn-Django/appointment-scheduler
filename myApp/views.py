from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views import generic, View
from .models import Appointment
from .forms import AppointmentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse


class IndexView(generic.TemplateView):
    template_name = "myApp/index.html"


class AppointmentFormView(LoginRequiredMixin, generic.CreateView):
    model = Appointment
    template_name = "myApp/appointment_form.html"
    form_class = AppointmentForm
    success_url = reverse_lazy('myApp:home')

    def form_valid(self, form):
        # Check if there is already an appointment at the same date and time for the user
        if Appointment.objects.filter(user=self.request.user, visited=False).exists():
            messages.warning(self.request, 'You have already had an ongoing appointment!')
            return redirect('myApp:home')

        # If no conflict, save the appointment and show a success message
        form.instance.user = self.request.user
        messages.success(self.request, 'Your appointment has been reserved.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if Appointment.objects.filter(user=self.request.user, visited=False).exists():
            ctx['appointment'] = Appointment.objects.filter(user=self.request.user, visited=False).first()
        return ctx

class AppointmentListView(generic.ListView):
    model = Appointment
    template_name = "myApp/appointment_list.html"
    context_object_name = 'appointments'

    def get_queryset(self):
        return Appointment.objects.filter(user=self.request.user)


class AppointmentListJson(View):
    """Returns all apps in JSON format suitable for FullCalendar."""
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse([], safe=False)

        apps = Appointment.objects.filter(user=request.user)
        events = []
        for a in apps:
            events.append({
                'id': a.id,
                'title': a.details,
                'start': a.date.isoformat(),
                'allDay': False,
            })
        return JsonResponse(events, safe=False)


def get_available_minutes(request):
    hour = request.GET.get('hour')
    date = request.GET.get('date')

    if not hour or not date:
        return JsonResponse({'error': 'Missing date or hour'}, status=400)

    try:
        hour = int(hour)
    except ValueError:
        return JsonResponse({'error': 'Invalid hour'}, status=400)

    all_minutes = [10, 20, 30, 40, 50]
    taken_minutes = (Appointment.objects.filter(date=date, hour=hour).values_list('minute', flat=True))
    available = [m for m in all_minutes if m not in taken_minutes]
    return JsonResponse(available, safe=False)


def get_available_hours(request):
    date = request.GET.get('date')
    if not date:
        return JsonResponse({'error': 'Missing date'}, status=400)

    available_hours = [h for h in range(8, 17)]
    filtered_hours = [
        hour for hour in available_hours
        if Appointment.objects.filter(date=date, hour=hour).count() < 5
    ]
    return JsonResponse(filtered_hours, safe=False)


