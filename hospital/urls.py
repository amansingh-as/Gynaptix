from django.urls import path
from . import views

from .views import (
    doctor_status,
    patient_list,
    add_patient,
    edit_patient,
    delete_patient
)

urlpatterns = [
    path('doctor-status/', doctor_status, name='doctor_status'),

    path('patients/', patient_list, name='patient_list'),
    path('patients/add/', add_patient, name='add_patient'),
    path('patients/edit/<int:id>/', edit_patient, name='edit_patient'),
    path('patients/delete/<int:id>/', delete_patient, name='delete_patient'),

    path('reports/', views.report_list, name='report_list'),
    path('reports/add/', views.add_report, name='add_report'),

    path('patients/<int:id>/reports/', views.patient_reports, name='patient_reports'),

    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    
    path('verify-access/', views.verify_access, name='verify_access'),
    path('', views.home, name='home'),

    path('appointment/', views.appointment, name='appointment'),

    path('appointments/', views.appointment_list, name='appointment_list'),

    
    
]