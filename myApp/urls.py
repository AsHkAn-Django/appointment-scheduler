from django.urls import path
from . import views


app_name = 'myApp'

urlpatterns = [
    path('appointment_form/', views.AppointmentFormView.as_view(), name='appointment_form'),
    path('my-appointments/', views.AppointmentListView.as_view(), name='my_appointments'),
    path('json-appointments/', views.AppointmentListJson.as_view(), name='app_list_json'),
    path('get-available-minutes/', views.get_available_minutes, name='get_available_minutes'),
    path('', views.IndexView.as_view(), name='home'),
]