import 'package:dio/dio.dart';

import '../models/attendance_event.dart';

class ApiService {
  ApiService()
      : _dio = Dio(
          BaseOptions(
            baseUrl: 'http://10.0.2.2:8000/api',
            connectTimeout: const Duration(seconds: 10),
            receiveTimeout: const Duration(seconds: 10),
          ),
        );

  final Dio _dio;

  Future<AttendanceEvent> scanQr(String qrToken) async {
    final response = await _dio.post('/attendance/scan/', data: {'qr_token': qrToken});
    return AttendanceEvent.fromApi(response.data as Map<String, dynamic>);
  }

  Future<List<Map<String, dynamic>>> fetchWeeklyPayroll() async {
    final response = await _dio.get('/attendance/weekly-payroll/');
    return List<Map<String, dynamic>>.from(response.data as List);
  }
}
