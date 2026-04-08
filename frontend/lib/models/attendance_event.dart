class AttendanceEvent {
  final String employeeName;
  final String cedula;
  final String eventType;
  final DateTime? checkIn;
  final DateTime? checkOut;

  AttendanceEvent({
    required this.employeeName,
    required this.cedula,
    required this.eventType,
    required this.checkIn,
    required this.checkOut,
  });

  factory AttendanceEvent.fromApi(Map<String, dynamic> json) {
    final record = json['record'] as Map<String, dynamic>;
    final employee = record['employee'] as Map<String, dynamic>;

    return AttendanceEvent(
      employeeName: employee['full_name']?.toString() ?? '',
      cedula: employee['cedula']?.toString() ?? '',
      eventType: json['event_type']?.toString() ?? '',
      checkIn: record['check_in'] != null
          ? DateTime.tryParse(record['check_in'].toString())
          : null,
      checkOut: record['check_out'] != null
          ? DateTime.tryParse(record['check_out'].toString())
          : null,
    );
  }
}
