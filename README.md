# PROYECTO: APP MÓVIL CONTROL DE ASISTENCIA CON QR Y NÓMINA

## 1. Descripción general
Aplicación móvil (APK Android) para registrar la entrada y salida de empleados mediante código QR.

El sistema almacenará:
- Nombre
- Cédula
- Hora de entrada
- Hora de salida

Además, calculará automáticamente la nómina.

## 2. Funcionalidades
- Escaneo QR independiente (el empleado escanea desde un dispositivo)
- Registro automático de asistencia
- Notificación por WhatsApp (Meta)
- Reportes semanales
- Cálculo automático de nómina

## 3. Lógica de nómina
- Valor del día: **$60.000 COP**
- El sistema calcula automáticamente:
  - Días trabajados
  - Ausencias
  - Total a pagar

> Nota: Se indicó como ejemplo `7 días trabajados = $300.000`, pero con un valor diario de $60.000 el total sería $420.000.

## 4. Tecnologías
- **Frontend:** Flutter
- **Backend:** Django
- **Base de datos:** PostgreSQL
- **API:** REST

## 5. WhatsApp (gratis)
Se utilizará la plataforma de **Meta** para el envío de mensajes sin costo (según el plan y límites vigentes).

Permitirá enviar notificaciones automáticas al administrador.

## 6. Generación de APK
Comando de compilación:

```bash
flutter build apk
```
