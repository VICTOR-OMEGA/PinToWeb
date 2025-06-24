#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

const char* ssid = "Wi-Fi";
const char* password = "Passwd";

const char* serverUrl = "http://192.168.43.56:5000/api/pintoweb";

const int sensorPin = pin;  // GPIO36 for LDR

void setup() {
  Serial.begin(115200);
  delay(1000);

  WiFi.begin(ssid, password);
  Serial.print("Connecting to Wi-Fi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWi-Fi connected. IP: " + WiFi.localIP().toString());
}

void loop() {
  int sensorValue = analogRead(sensorPin);
  Serial.println("LDR Value: " + String(sensorValue));

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");

    StaticJsonDocument<200> json;
    json["sensor"] = "ldr";
    json["value"] = sensorValue;

    String payload;
    serializeJson(json, payload);

    int httpResponseCode = http.POST(payload);

    Serial.print("HTTP Response: ");
    Serial.println(httpResponseCode);
    http.end();
  } else {
    Serial.println("Wi-Fi not connected");
  }

  delay(5000); // Send every 5 seconds
}

