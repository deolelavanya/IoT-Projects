#include <WiFi.h>
#include <HTTPClient.h>

const char* WIFI_SSID = "Wokwi-GUEST";
const char* WIFI_PASS = "";

const char* FIREBASE_URL =
  "https://prototype-8cd99-default-rtdb.firebaseio.com/telemetry/latest.json";

void setup() {
  Serial.begin(115200);
  WiFi.begin(WIFI_SSID, WIFI_PASS);

  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi connected");
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    float temperature = 28.0 + random(-30, 30) / 10.0;
    int battery = random(70, 100);
    int rssi = WiFi.RSSI();

    String payload = "{";
    payload += "\"device_id\":\"DEV_001\",";
    payload += "\"temperature_c\":" + String(temperature, 1) + ",";
    payload += "\"battery_pct\":" + String(battery) + ",";
    payload += "\"rssi_dbm\":" + String(rssi) + ",";
    payload += "\"timestamp_ms\":" + String(millis());
    payload += "}";

    http.begin(FIREBASE_URL);
    http.addHeader("Content-Type", "application/json");

    int code = http.PUT(payload);
    Serial.println("HTTP Code: " + String(code));
    Serial.println(payload);

    http.end();
  }

  delay(5000);
}
