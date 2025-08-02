from django.urls import path
from . import views


app_name = 'myApp'

urlpatterns = [
    path('appointment_form/', views.AppointmentFormView.as_view(), name='appointment_form'),
    path('my-appointments/', views.AppointmentListView.as_view(), name='my_appointments'),
    path('json-appointments/', views.AppointmentListJson.as_view(), name='app_list_json'),
    path('get-available-minutes/', views.get_available_minutes, name='get_available_minutes'),
    path('get-available-hours/', views.get_available_hours, name='get_available_hours'),
    path('google-auth/', views.google_auth_init, name='google_auth_init'),
    path('oauth2callback/', views.google_auth_callback, name='google_auth_callback'),
    path('create-event/', views.create_event, name='create_event'),
    path('', views.IndexView.as_view(), name='home'),
]