# PinToWeb

**PinToWeb** is a simple full-stack IoT project that connects an ESP32 microcontroller to a web dashboard. It reads data from a sensor (LDR), sends it via HTTP POST to a Python backend, stores it in a database, and displays it in real-time on a web interface.

---

## Project Architecture

```txt
[LDR Sensor]
    │
[ESP32 Microcontroller]
    │  (HTTP POST / JSON)
    ▼
[Flask Backend API] ──► [SQLite Database]
    │
    ▼
[Frontend (HTML + JS Dashboard)]
