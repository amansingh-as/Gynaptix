from django.contrib import admin
from .models import Patient, Doctor, Report

admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Report)