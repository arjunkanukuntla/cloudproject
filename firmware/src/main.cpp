/*
 * Cloud Security Alert Lamp - ESP32 Firmware
 * Hardware: ESP32 Dev Module + Red LED (GPIO 4)
 * Protocol: AWS IoT Core over TLS MQTT (Port 8883)
 * Function: Blinks Red LED rapidly when a public S3 bucket is detected by AWS Lambda
 */

#include <Arduino.h>
#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

#include "config.h"

// Check if secrets.h exists, otherwise fall back to template warning
#if __has_include("secrets.h")
  #include "secrets.h"
#else
  #include "secrets.h.template"
  #warning "Using secrets.h.template! Please create include/secrets.h with your actual Wi-Fi and AWS IoT credentials."
#endif

// System Security States
enum SystemState {
  STATE_OK,           // System Secure: No public buckets detected
  STATE_ALERT,        // Security Threat: Public bucket detected!
  STATE_DISCONNECTED  // Network/Cloud link offline
};

// Global State Variables
SystemState currentState = STATE_DISCONNECTED;
unsigned long lastBlinkMs = 0;
bool ledPinState = false;
unsigned long lastMqttRetryMs = 0;

// Network Objects
WiFiClientSecure netClient;
PubSubClient mqttClient(netClient);

// Function Declarations
void setupWiFi();
void connectAWS();
void mqttCallback(char* topic, byte* payload, unsigned int length);
void updateLedStateMachine();
void setLedHardware(bool state);

void setup() {
  Serial.begin(SERIAL_BAUD);
  delay(1000);

  Serial.println("\n=============================================");
  Serial.println("   Cloud Security Alert Lamp - ESP32 Boot");
  Serial.println("=============================================");

  // Pin Initialization
  pinMode(RED_LED_PIN, OUTPUT);
  pinMode(STATUS_LED_PIN, OUTPUT);
  setLedHardware(false);
  digitalWrite(STATUS_LED_PIN, LOW);

  // Initialize Wi-Fi and TLS AWS IoT certificates
  setupWiFi();

  netClient.setCACert(AWS_CERT_CA);
  netClient.setCertificate(AWS_CERT_CRT);
  netClient.setPrivateKey(AWS_CERT_PRIVATE);

  mqttClient.setServer(AWS_IOT_ENDPOINT, MQTT_PORT);
  mqttClient.setCallback(mqttCallback);

  connectAWS();
}

void loop() {
  // Check Wi-Fi connection
  if (WiFi.status() != WL_CONNECTED) {
    currentState = STATE_DISCONNECTED;
    setupWiFi();
  }

  // Check MQTT connection
  if (!mqttClient.connected()) {
    currentState = STATE_DISCONNECTED;
    unsigned long currentMs = millis();
    if (currentMs - lastMqttRetryMs > MQTT_RECONNECT_DELAY_MS) {
      lastMqttRetryMs = currentMs;
      connectAWS();
    }
  } else {
    mqttClient.loop();
  }

  // Update LED Indicator state machine
  updateLedStateMachine();
}

void setupWiFi() {
  if (WiFi.status() == WL_CONNECTED) return;

  Serial.print("[WiFi] Connecting to SSID: ");
  Serial.println(WIFI_SSID);

  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  int retries = 0;
  while (WiFi.status() != WL_CONNECTED && retries < 20) {
    delay(500);
    Serial.print(".");
    digitalWrite(STATUS_LED_PIN, !digitalRead(STATUS_LED_PIN)); // Toggle status LED during setup
    retries++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n[WiFi] Connected successfully!");
    Serial.print("[WiFi] ESP32 IP Address: ");
    Serial.println(WiFi.localIP());
    digitalWrite(STATUS_LED_PIN, HIGH);
  } else {
    Serial.println("\n[WiFi] Connection failed. Will retry in loop.");
    digitalWrite(STATUS_LED_PIN, LOW);
  }
}

void connectAWS() {
  if (WiFi.status() != WL_CONNECTED) return;

  Serial.print("[AWS IoT] Connecting to endpoint: ");
  Serial.println(AWS_IOT_ENDPOINT);

  String clientId = "ESP32_AlertLamp_";
  clientId += String(random(0xffff), HEX);

  if (mqttClient.connect(clientId.c_str())) {
    Serial.println("[AWS IoT] Connected to AWS IoT Core over TLS!");
    mqttClient.subscribe(MQTT_TOPIC_ALERTS);
    Serial.print("[AWS IoT] Subscribed to topic: ");
    Serial.println(MQTT_TOPIC_ALERTS);

    // Default state on successful link setup
    if (currentState == STATE_DISCONNECTED) {
      currentState = STATE_OK;
    }

    // Publish heartbeat/discovery message
    StaticJsonDocument<128> doc;
    doc["device"] = "ESP32_Alert_Lamp";
    doc["status"] = "ONLINE";
    doc["ip"] = WiFi.localIP().toString();
    
    char buffer[128];
    serializeJson(doc, buffer);
    mqttClient.publish(MQTT_TOPIC_STATUS, buffer);

  } else {
    Serial.print("[AWS IoT] Failed connection, rc=");
    Serial.println(mqttClient.state());
  }
}

void mqttCallback(char* topic, byte* payload, unsigned int length) {
  Serial.println("\n---------------------------------------------");
  Serial.print("[MQTT Message Received] Topic: ");
  Serial.println(topic);

  // Parse JSON message payload
  StaticJsonDocument<512> doc;
  DeserializationError error = deserializeJson(doc, payload, length);

  if (error) {
    Serial.print("[JSON Error] Deserialization failed: ");
    Serial.println(error.f_str());
    return;
  }

  const char* status = doc["status"] | "UNKNOWN";
  int publicCount = doc["public_buckets_count"] | doc["count"] | 0;

  Serial.print("[Security Scanner Status]: ");
  Serial.println(status);
  Serial.print("[Public S3 Buckets Count]: ");
  Serial.println(publicCount);

  if (strcmp(status, "ALERT") == 0 || publicCount > 0) {
    currentState = STATE_ALERT;
    Serial.println(">>> DANGER ALERT: PUBLIC S3 BUCKET DETECTED! BLINKING RED LED! <<<");

    JsonArray buckets = doc["public_buckets"].as<JsonArray>();
    if (!buckets.isNull()) {
      Serial.println("[Exposed Buckets List]:");
      for (JsonVariant b : buckets) {
        Serial.print(" - ");
        Serial.println(b.as<const char*>());
      }
    }
  } else {
    currentState = STATE_OK;
    Serial.println(">>> SYSTEM SECURE: No public S3 buckets detected. Red LED OFF. <<<");
  }
  Serial.println("---------------------------------------------");
}

void updateLedStateMachine() {
  unsigned long currentMs = millis();

  switch (currentState) {
    case STATE_ALERT:
      // Rapid blinking when S3 security breach / public bucket detected
      if (currentMs - lastBlinkMs >= BLINK_INTERVAL_ALERT_MS) {
        lastBlinkMs = currentMs;
        ledPinState = !ledPinState;
        setLedHardware(ledPinState);
      }
      break;

    case STATE_OK:
      // Red LED completely OFF when cloud security is safe
      setLedHardware(false);
      break;

    case STATE_DISCONNECTED:
      // Slow heartbeat pulse when disconnected from network/cloud
      if (currentMs - lastBlinkMs >= BLINK_INTERVAL_SAFE_MS) {
        lastBlinkMs = currentMs;
        ledPinState = !ledPinState;
        setLedHardware(ledPinState);
      }
      break;
  }
}

void setLedHardware(bool state) {
  if (LED_ACTIVE_HIGH) {
    digitalWrite(RED_LED_PIN, state ? HIGH : LOW);
  } else {
    digitalWrite(RED_LED_PIN, state ? LOW : HIGH);
  }
}
