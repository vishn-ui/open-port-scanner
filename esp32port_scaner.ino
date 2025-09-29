// esp32_forward_serial.ino
// Reads one-line JSON from Serial (USB) and forwards it to HOST_URL via HTTP POST
// esp32_forward_serial.ino



#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "Vishnu";
const char* password = "var472005";

// Host endpoint to receive forwarded JSON
const char* HOST_URL = "http://192.168.29.59:5000/report";

void setup() {
  Serial.begin(115200);
  delay(100);

  Serial.print("Connecting to WiFi ");
  WiFi.begin(ssid, password);
  unsigned long start = millis();
  while (WiFi.status() != WL_CONNECTED) {
    delay(300);
    Serial.print(".");
    if (millis() - start > 20000) {
      Serial.println("\nWiFi connection timeout");
      break;
    }
  }
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nWiFi connected. IP: " + WiFi.localIP().toString());
  } else {
    Serial.println("\nWiFi not connected - will still read serial and try later.");
  }

  Serial.println("Ready. Send one-line JSON from PC over serial.");
}

String readLineFromSerial(unsigned long timeoutMs = 4000) {
  unsigned long start = millis();
  String s = "";
  while (millis() - start < timeoutMs) {
    while (Serial.available() > 0) {
      char c = (char)Serial.read();
      if (c == '\n') {
        return s;
      }
      s += c;
      // safety: don't accumulate excessively large strings
      if (s.length() > 16000) {
        return s;
      }
    }
    delay(5);
  }
  return s; // may be empty if timed out
}

bool sendToHost(const String &jsonPayload) {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("No WiFi - cannot send");
    return false;
  }
  HTTPClient http;
  http.begin(HOST_URL);
  http.addHeader("Content-Type", "application/json");
  int httpCode = http.POST(jsonPayload);
  if (httpCode > 0) {
    Serial.printf("HTTP POST -> code: %d\n", httpCode);
    String resp = http.getString();
    Serial.println("Host response: " + resp);
    http.end();
    return (httpCode >= 200 && httpCode < 300);
  } else {
    Serial.printf("HTTP POST failed, error: %s\n", http.errorToString(httpCode).c_str());
    http.end();
    return false;
  }
}

void loop() {
  Serial.println("Waiting for JSON on serial...");
  String jsonLine = readLineFromSerial(7000); // wait up to 7s for input
  if (jsonLine.length() < 3) {
    // timeout or empty
    delay(500);
    return;
  }

  Serial.println("Received JSON:");
  Serial.println(jsonLine);

  bool sent = sendToHost(jsonLine);
  if (sent) {
    Serial.println("Forwarded to host successfully.");
  } else {
    Serial.println("Forward failed. Will retry next loop.");
  }

  // small pause before next read
  delay(1000);
}
