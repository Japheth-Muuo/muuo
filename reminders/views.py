from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView  # This is crucial for using LoginView
from .models import Dosage
from .forms import DosageForm
from django.contrib.auth.decorators import login_required
#from twilio.rest import Client
from django.conf import settings
from background_task import background


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'  # Custom template for login
    redirect_authenticated_user = True  # Redirect authenticated users

    def get_success_url(self):
        return '/dashboard/'  # Redirect to dashboard after login

# Your other views remain here
@login_required
def dashboard(request):
    dosages = Dosage.objects.filter(user=request.user)
    return render(request, 'reminders/dashboard.html', {'dosages': dosages})

def home(request):
    return render(request, 'reminders/home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'reminders/register.html', {'form': form})

@login_required
def add_dosage(request):
    if request.method == 'POST':
        form = DosageForm(request.POST)
        if form.is_valid():
            dosage = form.save(commit=False)
            dosage.user = request.user
            dosage.save()

            # Schedule SMS reminders
            if dosage.time_1:
                schedule_sms_reminder(dosage.id, dosage.time_1.isoformat())
            if dosage.time_2:
                schedule_sms_reminder(dosage.id, dosage.time_2.isoformat())
            if dosage.time_3:
                schedule_sms_reminder(dosage.id, dosage.time_3.isoformat())
            if dosage.time_4:
                schedule_sms_reminder(dosage.id, dosage.time_4.isoformat())
            if dosage.time_5:
                schedule_sms_reminder(dosage.id, dosage.time_5.isoformat())

            return redirect('dashboard')
    else:
        form = DosageForm()
    return render(request, 'reminders/add_dosage.html', {'form': form})



def send_sms(phone_number, message):
    # Initialize Twilio client
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    # Send message
    client.messages.create(
        body=message,
        from_=settings.TWILIO_PHONE_NUMBER,  # Twilio phone number
        to=phone_number
    )

@background(schedule=60)  # Schedule the task in 60 seconds (you can adjust based on the real time)
def schedule_sms_reminder(dosage_id, time_of_day):
    from datetime import datetime, timedelta
    from .models import Dosage

    dosage = Dosage.objects.get(pk=dosage_id)
    current_time = datetime.now().time()

    # Check if the reminder is for the correct time
    if current_time >= time_of_day:
        message = f"Reminder: It's time to take {dosage.medication_name}."
        send_sms(dosage.phone_number, message)
