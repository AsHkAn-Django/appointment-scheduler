from django.urls import path
from . import views


app_name = 'myApp'

urlpatterns = [
    path('appointment_form/', views.AppointmentFormView.as_view(), name='appointment_form'),
    path('my-appointments/', views.AppointmentListView.as_view(), name='my_appointments'),
    path('', views.IndexView.as_view(), name='home'),
]