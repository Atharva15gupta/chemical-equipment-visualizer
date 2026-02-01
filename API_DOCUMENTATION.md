# API Documentation

Complete API reference for the Chemical Equipment Visualizer backend.

## Base URL

```
http://localhost:8000/api
```

## Authentication

All endpoints except registration and login require authentication using Django session authentication.

### Headers

```
Content-Type: application/json
```

For file uploads:
```
Content-Type: multipart/form-data
```

## Endpoints

### 1. User Registration

**Endpoint:** `POST /auth/register/`

**Description:** Register a new user account

**Authentication:** Not required

**Request Body:**
```json
{
  "username": "string",
  "password": "string",
  "email": "string (optional)"
}
```

**Success Response (201 Created):**
```json
{
  "message": "User created successfully",
  "username": "string"
}
```

**Error Response (400 Bad Request):**
```json
{
  "error": "Username already exists"
}
```

---

### 2. User Login

**Endpoint:** `POST /auth/login/`

**Description:** Authenticate user and create session

**Authentication:** Not required

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Success Response (200 OK):**
```json
{
  "message": "Login successful",
  "username": "string"
}
```

**Error Response (401 Unauthorized):**
```json
{
  "error": "Invalid credentials"
}
```

---

### 3. Upload CSV File

**Endpoint:** `POST /datasets/upload/`

**Description:** Upload and analyze a CSV file containing equipment data

**Authentication:** Required

**Request:** Multipart form data
- `file`: CSV file

**Success Response (201 Created):**
```json
{
  "message": "File uploaded successfully",
  "dataset_id": 1,
  "summary": {
    "total_count": 20,
    "avg_flowrate": 195.32,
    "avg_pressure": 11.45,
    "avg_temperature": 98.75,
    "type_distribution": {
      "Reactor": 4,
      "Pump": 5,
      "Heat Exchanger": 6,
      "Compressor": 2,
      "Mixer": 2,
      "Separator": 2,
      "Column": 2
    }
  },
  "data": [
    {
      "Equipment Name": "Reactor-A1",
      "Type": "Reactor",
      "Flowrate": 150.5,
      "Pressure": 8.2,
      "Temperature": 120
    },
    ...
  ]
}
```

**Error Response (400 Bad Request):**
```json
{
  "error": "No file provided"
}
```

```json
{
  "error": "File must be a CSV"
}
```

```json
{
  "error": "CSV must contain columns: Equipment Name, Type, Flowrate, Pressure, Temperature"
}
```

---

### 4. Get Upload History

**Endpoint:** `GET /datasets/history/`

**Description:** Retrieve the last 5 uploaded datasets for the authenticated user

**Authentication:** Required

**Success Response (200 OK):**
```json
[
  {
    "id": 5,
    "filename": "equipment_data_v2.csv",
    "uploaded_at": "2024-02-01T14:30:00Z",
    "total_count": 20,
    "avg_flowrate": 195.32,
    "avg_pressure": 11.45,
    "avg_temperature": 98.75,
    "type_distribution": {
      "Reactor": 4,
      "Pump": 5
    }
  },
  {
    "id": 4,
    "filename": "equipment_data.csv",
    "uploaded_at": "2024-02-01T13:15:00Z",
    "total_count": 18,
    "avg_flowrate": 188.50,
    "avg_pressure": 10.80,
    "avg_temperature": 95.20,
    "type_distribution": {
      "Reactor": 3,
      "Pump": 4
    }
  }
]
```

---

### 5. Download PDF Report

**Endpoint:** `GET /datasets/{id}/download_pdf/`

**Description:** Generate and download a PDF report for a specific dataset

**Authentication:** Required

**URL Parameters:**
- `id` (integer): Dataset ID

**Success Response (200 OK):**
- Content-Type: `application/pdf`
- Content-Disposition: `attachment; filename="report_{id}.pdf"`
- Binary PDF data

**Error Response (404 Not Found):**
```json
{
  "detail": "Not found."
}
```

**Error Response (500 Internal Server Error):**
```json
{
  "error": "Error generating PDF: {error_message}"
}
```

---

## Data Models

### Dataset

```python
{
  "id": integer,
  "user": integer (user_id),
  "filename": string,
  "uploaded_at": datetime,
  "total_count": integer,
  "avg_flowrate": float,
  "avg_pressure": float,
  "avg_temperature": float,
  "type_distribution": dict,
  "csv_file": string (file_path)
}
```

## CSV File Format

Required columns:
- `Equipment Name`: String
- `Type`: String
- `Flowrate`: Numeric
- `Pressure`: Numeric
- `Temperature`: Numeric

Example:
```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Reactor-A1,Reactor,150.5,8.2,120
Pump-B2,Pump,200.3,12.5,85
```

## Error Handling

### Standard Error Response Format

```json
{
  "error": "Error message description"
}
```

### HTTP Status Codes

- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required or failed
- `403 Forbidden`: Authenticated but not authorized
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

## Rate Limiting

Currently no rate limiting is implemented. In production, consider implementing rate limiting for security.

## CORS

CORS is enabled for all origins in development. In production, configure `CORS_ALLOWED_ORIGINS` in settings.

## Authentication Flow

1. User registers via `/auth/register/`
2. User logs in via `/auth/login/` - receives session cookie
3. Browser automatically includes session cookie in subsequent requests
4. Backend validates session and returns user-specific data

## Example Usage

### JavaScript (Fetch API)

```javascript
// Login
const response = await fetch('http://localhost:8000/api/auth/login/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  credentials: 'include',
  body: JSON.stringify({ username: 'user', password: 'pass' })
});

// Upload CSV
const formData = new FormData();
formData.append('file', fileInput.files[0]);

const uploadResponse = await fetch('http://localhost:8000/api/datasets/upload/', {
  method: 'POST',
  credentials: 'include',
  body: formData
});
```

### Python (Requests)

```python
import requests

session = requests.Session()

# Login
session.post(
    'http://localhost:8000/api/auth/login/',
    json={'username': 'user', 'password': 'pass'}
)

# Upload CSV
with open('data.csv', 'rb') as f:
    session.post(
        'http://localhost:8000/api/datasets/upload/',
        files={'file': f}
    )
```

## Notes

- All datetime values are in ISO 8601 format (UTC)
- File uploads limited to CSV format only
- Maximum 5 datasets stored per user (oldest are auto-deleted)
- PDF generation uses ReportLab library
- Session cookies are HttpOnly for security
