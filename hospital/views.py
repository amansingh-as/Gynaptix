from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Patient, Doctor, Report
from .forms import PatientForm, ReportForm

from django.conf import settings
from .forms import AccessCodeForm

from .forms import AppointmentForm

from django.shortcuts import redirect
from django.urls import reverse

from .models import Appointment

def appointment_list(request):
    query = request.GET.get('q')  # search input

    if query:
        appointments = Appointment.objects.filter(
            name__icontains=query
        ) | Appointment.objects.filter(
            phone__icontains=query
        )
    else:
        appointments = Appointment.objects.all()

    appointments = appointments.order_by('-date')

    return render(request, 'appointment_list.html', {
        'appointments': appointments,
        'query': query
    })

def access_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.session.get('access_granted'):
            return view_func(request, *args, **kwargs)
        return redirect(f'/verify-access/?next={request.path}')
    return wrapper

def verify_access(request):
    form = AccessCodeForm(request.POST or None)

    if form.is_valid():
        if form.cleaned_data['code'] == settings.ACCESS_CODE:
            request.session['access_granted'] = True
            next_url = request.GET.get('next')
            return redirect(next_url)

    return render(request, 'hospital/access_code.html', {'form': form})


@login_required
def doctor_dashboard(request):
    try:
        doctor = Doctor.objects.get(user=request.user)
    except Doctor.DoesNotExist:
        return redirect('login')  # or show error page

    reports = Report.objects.filter(doctor=doctor)
    
    return render(request, 'hospital/doctor_dashboard.html', {
        'doctor': doctor,
        'reports': reports
    })

def patient_list(request):
    query = request.GET.get('q')

    if query:
        patients = Patient.objects.filter(
            name__icontains=query
        ) | Patient.objects.filter(
            phone__icontains=query
        )
    else:
        patients = Patient.objects.all()

    return render(request, 'hospital/patient_list.html', {'patients': patients})


@login_required
@access_required
def add_patient(request):
    form = PatientForm(request.POST or None)

    if form.is_valid():
        form.save()
        request.session['access_granted'] = False
        return redirect('patient_list')

    return render(request, 'hospital/add_patient.html', {'form': form})


@login_required
@access_required
def edit_patient(request, id):
    patient = get_object_or_404(Patient, id=id)
    form = PatientForm(request.POST or None, instance=patient)

    if form.is_valid():
        form.save()
        request.session['access_granted'] = False
        return redirect('patient_list')

    return render(request, 'hospital/add_patient.html', {'form': form})


@login_required
@access_required
def delete_patient(request, id):
    patient = get_object_or_404(Patient, id=id)
    patient.delete()
    request.session['access_granted'] = False
    return redirect('patient_list')


@login_required
def doctor_status(request):
    present = Doctor.objects.filter(is_present=True).count()
    absent = Doctor.objects.filter(is_present=False).count()

    return JsonResponse({
        'present': present,
        'absent': absent
    })


@login_required
@access_required
def add_report(request):
    form = ReportForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        request.session['access_granted'] = False
        return redirect('report_list')

    return render(request, 'hospital/add_report.html', {'form': form})

@login_required
def report_list(request):
    reports = Report.objects.select_related('patient', 'doctor')
    return render(request, 'hospital/report_list.html', {'reports': reports})

@login_required
def patient_reports(request, id):
    patient = get_object_or_404(Patient, id=id)
    reports = patient.reports.all()   

    return render(request, 'hospital/patient_reports.html', {
        'patient': patient,
        'reports': reports
    })

def home(request):
    return render(request, 'home.html')


def appointment(request):
    success = False

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            success = True
            form = AppointmentForm()  # reset form
    else:
        form = AppointmentForm()

    return render(request, 'appointment.html', {
        'form': form,
        'success': success
    })