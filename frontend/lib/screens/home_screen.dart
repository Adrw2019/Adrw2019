import 'package:flutter/material.dart';
import 'package:mobile_scanner/mobile_scanner.dart';

import '../models/attendance_event.dart';
import '../services/api_service.dart';
import 'check_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final ApiService _api = ApiService();
  bool _processing = false;
  String? _error;
  List<Map<String, dynamic>> _payroll = [];

  Future<void> _loadPayroll() async {
    try {
      final data = await _api.fetchWeeklyPayroll();
      setState(() => _payroll = data);
    } catch (e) {
      setState(() => _error = 'No se pudo cargar nómina: $e');
    }
  }

  Future<void> _processScan(String token) async {
    if (_processing) return;
    setState(() {
      _processing = true;
      _error = null;
    });

    try {
      final AttendanceEvent event = await _api.scanQr(token);
      if (!mounted) return;
      await Navigator.push(
        context,
        MaterialPageRoute(builder: (_) => CheckResultScreen(event: event)),
      );
      await _loadPayroll();
    } catch (e) {
      setState(() => _error = 'Error registrando asistencia: $e');
    } finally {
      if (mounted) {
        setState(() => _processing = false);
      }
    }
  }

  @override
  void initState() {
    super.initState();
    _loadPayroll();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Asistencia QR y Nómina')),
      body: Column(
        children: [
          Expanded(
            flex: 4,
            child: Stack(
              children: [
                MobileScanner(
                  onDetect: (capture) {
                    final barcode = capture.barcodes.firstOrNull;
                    final token = barcode?.rawValue;
                    if (token != null && token.isNotEmpty) {
                      _processScan(token);
                    }
                  },
                ),
                if (_processing)
                  const Center(
                    child: ColoredBox(
                      color: Colors.black45,
                      child: Padding(
                        padding: EdgeInsets.all(12),
                        child: CircularProgressIndicator(),
                      ),
                    ),
                  ),
              ],
            ),
          ),
          Expanded(
            flex: 3,
            child: Padding(
              padding: const EdgeInsets.all(12),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('Reporte semanal de nómina', style: Theme.of(context).textTheme.titleLarge),
                  const SizedBox(height: 8),
                  if (_error != null)
                    Text(_error!, style: const TextStyle(color: Colors.red)),
                  const SizedBox(height: 8),
                  Expanded(
                    child: ListView.builder(
                      itemCount: _payroll.length,
                      itemBuilder: (context, index) {
                        final row = _payroll[index];
                        return Card(
                          child: ListTile(
                            title: Text(row['employee_name'].toString()),
                            subtitle: Text('Días: ${row['worked_days']} | Ausencias: ${row['absent_days']}'),
                            trailing: Text('\$${row['total_pay']}'),
                          ),
                        );
                      },
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
