#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "your_wifi_ssid";
const char* password = "your_wifi_password";
const char* serverName = "http://192.168.1.100:5000/api/server_name";

const int ldrPin = A0;

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
}

void loop() {
  int ldrValue = analogRead(ldrPin);
  String jsonPayload = "{\"sensor\":\"ldr\",\"value\":" + String(ldrValue) + ",\"timestamp\":\"" + getTimestamp() + "\"}";

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverName);
    http.addHeader("Content-Type", "application/json");
    int httpResponseCode = http.POST(jsonPayload);
    http.end();
  }

  delay(10000); // Send every 10 seconds
}

String getTimestamp() {
  // Dummy static timestamp for now (ESP32 without RTC or NTP)
  return "2025-06-24T02:00:00";
}

