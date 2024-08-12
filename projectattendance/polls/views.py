from django.shortcuts import render

# Create your views here.
# attendance/views.py
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Employee, AttendanceRecord
from .forms import AttendanceForm
# attendance/views.py
import pandas as pd
from django.http import HttpResponse
from django.utils.timezone import localtime

def check_in_view(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('attendance:check_in')
    else:
        form = AttendanceForm()
    return render(request, 'attendance/check_in.html', {'form': form})

def check_out_view(request, record_id):
    record = AttendanceRecord.objects.get(id=record_id)
    record.check_out = timezone.now()
    record.save()
    return redirect('attendance:check_in')

def attendance_report_view(request):
    employees = Employee.objects.all()
    return render(request, 'attendance/report.html', {'employees': employees})


def generate_report_view(request):
    records = AttendanceRecord.objects.all()

    data = []
    for record in records:
        check_in = localtime(record.check_in).replace(tzinfo=None) if record.check_in else None
        check_out = localtime(record.check_out).replace(tzinfo=None) if record.check_out else None

        data.append({
            'Employee': record.employee.name,
            'Check In': check_in,
            'Check Out': check_out,
            'Working Hours': record.working_hours(),
        })

    df = pd.DataFrame(data)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=attendance_report.xlsx'
    df.to_excel(response, index=False)
    return response



