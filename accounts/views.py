from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import RegisterForm, LoginForm
from .models import User
from django.contrib.auth.decorators import login_required
from hospital.models import Doctor, Report



@login_required
def admin_dashboard(request):
    return render(request, 'dashboard/admin_dashboard.html')


@login_required
def doctor_dashboard(request):
    try:
        doctor = Doctor.objects.get(user=request.user)
    except Doctor.DoesNotExist:
        return redirect('login')

    reports = Report.objects.filter(doctor=doctor)

    return render(request, 'dashboard/doctor_dashboard.html', {
        'doctor': doctor,
        'reports': reports
    })


@login_required
def patient_dashboard(request):
    return render(request, 'dashboard/patient_dashboard.html')


@login_required
def staff_dashboard(request):
    return render(request, 'dashboard/staff_dashboard.html')


def register_view(request):
    form = RegisterForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return redirect('login')

    return render(request, 'register.html', {'form': form})


def login_view(request):
    form = LoginForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            # 🔥 ROLE BASED REDIRECT
            if user.role == 'admin':
                return redirect('admin_dashboard')
            #elif user.role == 'doctor':
                #doctor, created = Doctor.objects.get_or_create(user=user)

               # return redirect('doctor_dashboard')
            elif user.role == 'patient':
                return redirect('patient_dashboard')
            else:
                return redirect('staff_dashboard')

    return render(request, 'login.html', {'form': form})

def access_code_view(request):
    if request.method == 'POST':
        code = request.POST.get('code')

        if code == '12345':
            request.session['access_granted'] = True  

            next_url = request.session.get('next_url', '/')
            return redirect(next_url)

        else:
            return render(request, 'access_code.html', {
                'error': 'Invalid Access Code'
            })

    return render(request, 'access_code.html')