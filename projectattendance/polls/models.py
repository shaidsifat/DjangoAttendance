from django.db import models

# Create your models here.
# attendance/models.py
from django.db import models
from django.utils import timezone

class Employee(models.Model):
    name = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

class AttendanceRecord(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField(null=True, blank=True)

    def working_hours(self):
        if self.check_out:
            return (self.check_out - self.check_in).total_seconds() / 3600
        return 0
