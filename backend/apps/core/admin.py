from django.contrib import admin
from .models import AttendanceRecord, Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'cedula', 'phone_number', 'is_active')
    search_fields = ('full_name', 'cedula', 'phone_number')


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'date', 'check_in', 'check_out')
    list_filter = ('date',)
    search_fields = ('employee__full_name', 'employee__cedula')
