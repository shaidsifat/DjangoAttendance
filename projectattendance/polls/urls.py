# attendance/urls.py
from django.urls import path
from .views import check_in_view, check_out_view, attendance_report_view

app_name = 'polls'
from .views import generate_report_view
urlpatterns = [
    path('check_in/', check_in_view, name='check_in'),
    path('check_out/<int:record_id>/', check_out_view, name='check_out'),
    path('report/', attendance_report_view, name='report'),
]
urlpatterns += [
    path('generate_report/', generate_report_view, name='generate_report'),
]