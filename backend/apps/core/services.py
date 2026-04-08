from datetime import datetime, timedelta
import requests
from django.conf import settings
from django.db.models import Q
from django.utils import timezone

from .models import AttendanceRecord, Employee


def process_qr_scan(qr_token: str):
    employee = Employee.objects.filter(qr_token=qr_token, is_active=True).first()
    if not employee:
        raise ValueError('Empleado no encontrado o inactivo.')

    local_now = timezone.localtime()
    record, _ = AttendanceRecord.objects.get_or_create(employee=employee, date=local_now.date())

    event_type = 'unknown'
    if record.check_in is None:
        record.check_in = local_now
        event_type = 'check_in'
    elif record.check_out is None:
        record.check_out = local_now
        event_type = 'check_out'
    else:
        raise ValueError('El empleado ya registró entrada y salida hoy.')

    record.save()
    notify_admin_whatsapp(employee, event_type, local_now)
    return record, event_type


def weekly_payroll(reference_date=None):
    if reference_date is None:
        reference_date = timezone.localdate()

    start_of_week = reference_date - timedelta(days=reference_date.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    payload = []
    for employee in Employee.objects.filter(is_active=True):
        records = AttendanceRecord.objects.filter(
            employee=employee,
            date__range=(start_of_week, end_of_week),
        )
        worked_days = records.filter(~Q(check_in=None), ~Q(check_out=None)).count()
        absent_days = 7 - worked_days
        total_pay = worked_days * settings.DAILY_RATE

        payload.append(
            {
                'employee_id': employee.id,
                'employee_name': employee.full_name,
                'cedula': employee.cedula,
                'worked_days': worked_days,
                'absent_days': absent_days,
                'daily_rate': settings.DAILY_RATE,
                'total_pay': total_pay,
                'week_start': start_of_week,
                'week_end': end_of_week,
            }
        )
    return payload


def notify_admin_whatsapp(employee: Employee, event_type: str, event_time: datetime):
    token = settings.META_WHATSAPP_TOKEN
    phone_id = settings.META_WHATSAPP_PHONE_ID
    admin_number = settings.META_WHATSAPP_ADMIN_NUMBER

    if not token or not phone_id or not admin_number:
        return

    event_human = 'ENTRADA' if event_type == 'check_in' else 'SALIDA'
    body = (
        f'Asistencia registrada: {event_human}\n'
        f'Empleado: {employee.full_name}\n'
        f'Cédula: {employee.cedula}\n'
        f'Hora: {event_time.strftime("%Y-%m-%d %H:%M:%S")}'
    )

    url = f'https://graph.facebook.com/v22.0/{phone_id}/messages'
    response = requests.post(
        url,
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
        },
        json={
            'messaging_product': 'whatsapp',
            'to': admin_number,
            'type': 'text',
            'text': {'body': body},
        },
        timeout=8,
    )
    response.raise_for_status()
