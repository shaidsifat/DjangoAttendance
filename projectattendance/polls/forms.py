# attendance/forms.py
from django import forms
from .models import AttendanceRecord

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = AttendanceRecord
        fields = ['employee', 'check_in', 'check_out']
