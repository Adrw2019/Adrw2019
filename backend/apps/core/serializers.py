from rest_framework import serializers
from .models import AttendanceRecord, Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'full_name', 'cedula', 'phone_number', 'qr_token', 'is_active']


class AttendanceRecordSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)

    class Meta:
        model = AttendanceRecord
        fields = ['id', 'employee', 'date', 'check_in', 'check_out', 'notes']


class ScanQRSerializer(serializers.Serializer):
    qr_token = serializers.CharField(max_length=64)
