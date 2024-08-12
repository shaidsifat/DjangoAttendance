# attendance/tasks.py
import pandas as pd
from django.utils.timezone import localtime
from django.core.mail import EmailMessage
from django.http import HttpResponse
from .models import AttendanceRecord
from celery import shared_task
from io import BytesIO

@shared_task
def generate_and_send_report():
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
    output = BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)

    # Send email
    email = EmailMessage(
        subject="Weekly Attendance Report",
        body="Please find the attached weekly attendance report.",
        from_email="shaidsifat55@gmail.com",
        to=["sifat15-7616@diu.gmail.com"],
    )
    email.attach('attendance_report.xlsx', output.read(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    email.send()
