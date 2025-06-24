# Microcontroller Firmware - PinToWeb

This folder contains the code for the mcu device.

## Function

- Reads analog values from an LDR sensor
- Connects to Wi-Fi
- Formats sensor readings as JSON
- Sends data via HTTP POST to the backend Flask API every X seconds

## Hardware Setup

- Analog_sensor connected to analog pin `A0` (GPIO36 or GPIO34 depending on your mcu)
- Wi-Fi credentials defined in code
- No cloud dependency — sends data to local network

## How to Use

1. Open `main.ino` in Arduino IDE
2. Enter your Wi-Fi SSID and password
3. Upload to mcu
4. Ensure the backend is running and accessible on the same network

