# Flask Backend - PinToWeb

This folder contains the backend API service for receiving and storing sensor data.

## Function

- Accepts HTTP POST data from mcu at `/api/name`
- Stores readings in an SQLite database (`sensor_data.db`)
- Provides a GET route at `/api/name/data` for retrieving latest entries

## Routes

### POST `/api/name`

Accepts JSON payload:
```json
{
  "sensor": "ldr",
  "value": 723,
  "timestamp": "2025-06-24T02:00:00"
}
