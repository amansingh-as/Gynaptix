from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Patient(models.Model):

    

    name = models.CharField(max_length=100)
    age = models.IntegerField()

    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )

    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=15, unique=True)
    address = models.TextField()
    medical_history = models.TextField()

    def __str__(self):
        return self.name
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    experience = models.IntegerField(help_text="Years of experience")
    is_present = models.BooleanField(default=True)

    def __str__(self):
        return f"Doctor: {self.user}"


class Report(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='reports')
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)

    title = models.CharField(max_length=200)
    description = models.TextField()

    file = models.FileField(upload_to='reports/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.patient.name}"
    
class Appointment(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    phone = models.CharField(max_length=15)

    email = models.EmailField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)

    date = models.DateTimeField(auto_now_add=True)  # auto date + time

    def __str__(self):
        return self.name