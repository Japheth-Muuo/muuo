from django import forms
from .models import Dosage

class DosageForm(forms.ModelForm):
    class Meta:
        model = Dosage
        fields = ['medication_name', 'dosage', 'number_of_times', 'time_1', 'time_2', 'time_3', 'time_4', 'time_5', 'phone_number']
        widgets = {
            'time_1': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
            'time_2': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
            'time_3': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
            'time_4': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
            'time_5': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        number_of_times = cleaned_data.get('number_of_times')
        time_1 = cleaned_data.get('time_1')
        time_2 = cleaned_data.get('time_2')
        time_3 = cleaned_data.get('time_3')
        time_4 = cleaned_data.get('time_4')
        time_5 = cleaned_data.get('time_5')

        # Validate that the number of times corresponds to the number of time fields filled
        if number_of_times >= 1 and not time_1:
            self.add_error('time_1', 'Please provide at least one time.')
        if number_of_times >= 2 and not time_2:
            self.add_error('time_2', 'Please provide a second time for twice a day dosage.')
        if number_of_times >= 3 and not time_3:
            self.add_error('time_3', 'Please provide a third time for three times a day dosage.')
        if number_of_times >= 4 and not time_4:
            self.add_error('time_4', 'Please provide a fourth time for four times a day dosage.')
        if number_of_times == 5 and not time_5:
            self.add_error('time_5', 'Please provide a fifth time for five times a day dosage.')
