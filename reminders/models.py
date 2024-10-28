from django.db import models
from django.contrib.auth.models import User

class Dosage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    medication_name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100)
    number_of_times = models.PositiveIntegerField(default=1)  # Number of times per day (1 to 5)
    time_1 = models.TimeField(null=True, blank=True)  # First time
    time_2 = models.TimeField(null=True, blank=True)  # Second time (optional)
    time_3 = models.TimeField(null=True, blank=True)  # Third time (optional)
    time_4 = models.TimeField(null=True, blank=True)  # Fourth time (optional)
    time_5 = models.TimeField(null=True, blank=True)  # Fifth time (optional)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.medication_name} for {self.user.username}"
