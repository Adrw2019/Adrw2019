from django.db import models


class Employee(models.Model):
    full_name = models.CharField(max_length=255)
    cedula = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=20, blank=True)
    qr_token = models.CharField(max_length=64, unique=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['full_name']

    def __str__(self):
        return f'{self.full_name} ({self.cedula})'


class AttendanceRecord(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendance')
    date = models.DateField()
    check_in = models.DateTimeField(null=True, blank=True)
    check_out = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['employee', 'date'], name='unique_employee_daily_attendance'),
        ]
        ordering = ['-date', 'employee__full_name']

    def __str__(self):
        return f'{self.employee.full_name} - {self.date}'
