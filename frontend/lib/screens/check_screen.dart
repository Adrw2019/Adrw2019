import 'package:flutter/material.dart';

import '../models/attendance_event.dart';

class CheckResultScreen extends StatelessWidget {
  const CheckResultScreen({super.key, required this.event});

  final AttendanceEvent event;

  @override
  Widget build(BuildContext context) {
    final isIn = event.eventType == 'check_in';

    return Scaffold(
      appBar: AppBar(title: const Text('Registro procesado')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Card(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  isIn ? '✅ Entrada registrada' : '✅ Salida registrada',
                  style: Theme.of(context).textTheme.headlineSmall,
                ),
                const SizedBox(height: 12),
                Text('Empleado: ${event.employeeName}'),
                Text('Cédula: ${event.cedula}'),
                const SizedBox(height: 16),
                Text('Hora entrada: ${event.checkIn?.toLocal().toString() ?? '-'}'),
                Text('Hora salida: ${event.checkOut?.toLocal().toString() ?? '-'}'),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
