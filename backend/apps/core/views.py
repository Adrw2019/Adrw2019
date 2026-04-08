from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import AttendanceRecord, Employee
from .serializers import AttendanceRecordSerializer, EmployeeSerializer, ScanQRSerializer
from .services import process_qr_scan, weekly_payroll


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filterset_fields = ['is_active']
    search_fields = ['full_name', 'cedula']


class AttendanceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AttendanceRecord.objects.select_related('employee').all()
    serializer_class = AttendanceRecordSerializer
    filterset_fields = ['date', 'employee__id', 'employee__cedula']

    @action(detail=False, methods=['post'], url_path='scan')
    def scan_qr(self, request):
        serializer = ScanQRSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            record, event_type = process_qr_scan(serializer.validated_data['qr_token'])
        except ValueError as error:
            return Response({'detail': str(error)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({'detail': f'Error interno: {error}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(
            {
                'event_type': event_type,
                'record': AttendanceRecordSerializer(record).data,
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=['get'], url_path='weekly-payroll')
    def weekly_payroll_report(self, request):
        return Response(weekly_payroll(), status=status.HTTP_200_OK)
