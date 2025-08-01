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
    form_class = AppointmentForm
    template_name = "myApp/appointment_form.html"
    success_url = reverse_lazy('myApp:home')

    def form_valid(self, form):
        # before saving, check for any existing ongoing appointment
        if Appointment.objects.filter(user=self.request.user, visited=False).exists():
            # add a non-field error and re-render the form
            form.add_error(None, "You already have an ongoing appointment.")
            return self.form_invalid(form)

        # no conflict: attach user and save
        form.instance.user = self.request.user
        messages.success(self.request, "Your appointment has been reserved.")
        return super().form_valid(form)

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
                'title': f"Appointment at {a.get_time()}",
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


