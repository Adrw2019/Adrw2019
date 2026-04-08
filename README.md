# APP MÓVIL: CONTROL DE ASISTENCIA CON QR Y NÓMINA

Este repositorio ahora contiene una **arquitectura completa base (frontend + backend)** para tu proyecto:

- **Frontend móvil:** Flutter (Android APK)
- **Backend:** Django + Django REST Framework
- **Base de datos:** PostgreSQL
- **Notificaciones:** WhatsApp Cloud API (Meta)

---

## 1) Arquitectura propuesta

```text
[Empleado (App Flutter)]
      │ escanea QR
      ▼
[API Django REST]
  - valida qr_token
  - registra ENTRADA/SALIDA
  - guarda asistencia en PostgreSQL
  - calcula nómina semanal
  - envía notificación a WhatsApp (Meta)
      │
      ▼
[Administrador]
  - recibe alertas por WhatsApp
  - consulta reporte semanal de nómina
```

### Componentes
- `frontend/`: app móvil Android (scanner QR + reporte semanal).
- `backend/`: API REST para empleados, asistencia y nómina.
- PostgreSQL: persistencia de empleados y registros diarios.

---

## 2) Estructura del repositorio

```text
backend/
  config/
  apps/core/
    models.py
    views.py
    services.py
    serializers.py
frontend/
  lib/
    screens/
    services/
    models/
README.md
```

---

## 3) Funcionalidades implementadas en código

### Backend (Django)
- CRUD de empleados (`/api/employees/`)
- Registro de asistencia por escaneo QR (`POST /api/attendance/scan/`)
- Reporte semanal de nómina (`GET /api/attendance/weekly-payroll/`)
- Cálculo automático:
  - `valor_dia = 60.000` (configurable)
  - `worked_days`
  - `absent_days`
  - `total_pay = worked_days * valor_dia`
- Integración con WhatsApp Cloud API (Meta) para alertas al administrador.

### Frontend (Flutter)
- Escáner QR con `mobile_scanner`
- Envío del token escaneado al backend
- Pantalla de resultado de entrada/salida
- Visualización de reporte semanal de nómina

---

## 4) Modelo de datos principal

### `Employee`
- `full_name`
- `cedula` (único)
- `phone_number`
- `qr_token` (único)
- `is_active`

### `AttendanceRecord`
- `employee` (FK)
- `date`
- `check_in`
- `check_out`
- Restricción única por empleado/día

---

## 5) Endpoints REST

### Empleados
- `GET /api/employees/`
- `POST /api/employees/`
- `GET /api/employees/{id}/`
- `PUT/PATCH /api/employees/{id}/`
- `DELETE /api/employees/{id}/`

### Asistencia
- `POST /api/attendance/scan/`

Request:
```json
{
  "qr_token": "TOKEN_UNICO_DEL_EMPLEADO"
}
```

Response (ejemplo):
```json
{
  "event_type": "check_in",
  "record": {
    "id": 1,
    "employee": {
      "id": 1,
      "full_name": "Juan Pérez",
      "cedula": "12345678",
      "phone_number": "3001112233",
      "qr_token": "abc123",
      "is_active": true
    },
    "date": "2026-04-08",
    "check_in": "2026-04-08T08:01:10-05:00",
    "check_out": null,
    "notes": ""
  }
}
```

### Nómina semanal
- `GET /api/attendance/weekly-payroll/`

---

## 6) Configuración Backend

### Variables de entorno (`backend/.env`)
Copiar desde `backend/.env.example`:

```env
DJANGO_SECRET_KEY=change-me
DJANGO_DEBUG=true
DJANGO_ALLOWED_HOSTS=*
TIME_ZONE=America/Bogota
DAILY_RATE=60000

POSTGRES_DB=attendance_db
POSTGRES_USER=attendance_user
POSTGRES_PASSWORD=attendance_pass
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

META_WHATSAPP_TOKEN=
META_WHATSAPP_PHONE_ID=
META_WHATSAPP_ADMIN_NUMBER=573001112233
```

### Instalación y ejecución

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## 7) Configuración Frontend (Flutter)

```bash
cd frontend
flutter pub get
flutter run
```

> En emulador Android, la API local usa `http://10.0.2.2:8000`.

Generar APK:

```bash
flutter build apk
```

---

## 8) WhatsApp Cloud API (Meta)

La integración ya está preparada en `backend/apps/core/services.py`.

Para activarla:
1. Crear app en Meta Developers.
2. Habilitar WhatsApp Cloud API.
3. Configurar `META_WHATSAPP_TOKEN`, `META_WHATSAPP_PHONE_ID` y `META_WHATSAPP_ADMIN_NUMBER`.

---

## 9) Nota sobre lógica de pago

Con `valor_dia = $60.000`, entonces:

- **7 días trabajados = $420.000**

Si deseas mantener `7 días = $300.000`, debes cambiar `DAILY_RATE=42857` o redefinir la regla de negocio.

---

## 10) Próximos pasos recomendados

- Autenticación JWT para app/admin.
- Roles (admin/supervisor/empleado).
- Cierre de nómina por periodos quincenales/mensuales.
- Exportación a Excel/PDF.
- Geolocalización/foto para validación anti-fraude.
- Pruebas unitarias e integración CI/CD.
