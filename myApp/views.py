from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse, HttpResponseBadRequest
from django.conf import settings

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow

from .models import Appointment
from .forms import AppointmentForm
from datetime import datetime, time, timedelta
import os


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


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



def google_auth_init(request):
    flow = Flow.from_client_secrets_file(
        str(settings.GOOGLE_CREDENTIALS_FILE),  # use absolute path from settings
        scopes=settings.GOOGLE_SCOPES,
        redirect_uri=settings.GOOGLE_REDIRECT_URI  # keep redirect URI consistent
    )
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    request.session['state'] = state
    request.session.save()  # Ensure session saved before redirect
    return redirect(authorization_url)


def google_auth_callback(request):
    state = request.session.get('state')
    if not state:
        return HttpResponseBadRequest("Session expired or invalid state. Please start the authentication process again.")

    flow = Flow.from_client_secrets_file(
        str(settings.GOOGLE_CREDENTIALS_FILE),
        scopes=settings.GOOGLE_SCOPES,
        state=state,
        redirect_uri=settings.GOOGLE_REDIRECT_URI
    )
    flow.fetch_token(authorization_response=request.build_absolute_uri())

    credentials = flow.credentials

    # Store credentials in session or preferably database (demo: session)
    request.session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
    request.session.save()
    return redirect('myApp:create_event')


def create_event(request, pk):
    if 'credentials' not in request.session:
        return redirect('myApp:google_auth_init')

    creds = Credentials(**request.session['credentials'])
    service = build('calendar', 'v3', credentials=creds)

    appointment = get_object_or_404(Appointment, pk=pk)

    start_time = time(appointment.hour, appointment.minute)
    start_datetime = datetime.combine(appointment.date, start_time)

    end_datetime = start_datetime + timedelta(minutes=10)

    event = {
        'summary': appointment.details or 'Test Appointment',
        'description': appointment.details or 'A Test Appointment',
        'start': {
            'dateTime': start_datetime.isoformat(),
            'timeZone': 'Europe/Istanbul',
        },
        'end': {
            'dateTime': end_datetime.isoformat(),
            'timeZone': 'Europe/Istanbul',
        },
    }

    event_result = service.events().insert(calendarId='primary', body=event).execute()
    return render(request, 'myApp/event_success.html', {'event': event_result})