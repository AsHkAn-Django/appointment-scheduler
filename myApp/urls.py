from django.urls import path
from . import views


app_name = 'myApp'
urlpatterns = [
    path('appointment_form/', views.AppointmentFormView.as_view(), name='appointment_form'),
    path('', views.IndexView.as_view(), name='home'),
]