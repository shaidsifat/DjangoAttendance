# attendance/admin.py
import pandas as pd
from django.http import HttpResponse
from django.utils.timezone import localtime
from django.contrib import admin
from .models import Employee, AttendanceRecord

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'employee_id')
    search_fields = ('name', 'employee_id')
    ordering = ('name',)

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('employee', 'check_in', 'check_out', 'working_hours')
    list_filter = ('employee', 'check_in', 'check_out')
    search_fields = ('employee__name', 'employee__employee_id')
    ordering = ('-check_in',)
    actions = ['generate_excel_report']

    def working_hours(self, obj):
        return obj.working_hours()
    working_hours.short_description = 'Working Hours (hrs)'

    def generate_excel_report(self, request, queryset):
        # This action generates and returns the Excel report
        data = []
        for record in queryset:
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

    generate_excel_report.short_description = "Generate Excel Report"

