from django.urls import path
from .views import (
    register_view, login_view,
    admin_dashboard, doctor_dashboard,
    patient_dashboard, staff_dashboard,
    access_code_view

    
)

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),

    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('doctor-dashboard/', doctor_dashboard, name='doctor_dashboard'),
    path('patient-dashboard/', patient_dashboard, name='patient_dashboard'),
    path('staff-dashboard/', staff_dashboard, name='staff_dashboard'),
    path('access-code/', access_code_view, name='access_code'),
]