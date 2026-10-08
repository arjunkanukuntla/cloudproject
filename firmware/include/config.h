#ifndef CONFIG_H
#define CONFIG_H

// ==========================================
// Hardware Pin Configuration
// ==========================================
// GPIO pin connected to the external Red Alert LED (anode via 220 Ohm resistor)
#define RED_LED_PIN 4

// Onboard ESP32 status LED (GPIO 2 on most ESP32 DevKits)
#define STATUS_LED_PIN 2

// Active HIGH logic: set to 1 if HIGH turns LED on, 0 if LOW turns LED on
#define LED_ACTIVE_HIGH 1

// ==========================================
// MQTT & Network Configuration
// ==========================================
#define MQTT_PORT 8883
#define MQTT_TOPIC_ALERTS "cloud/security/alerts"
#define MQTT_TOPIC_STATUS "cloud/security/device/status"

// Serial console baud rate
#define SERIAL_BAUD 115200

// ==========================================
// Timing & Blink Configuration
// ==========================================
// Rapid blink interval when S3 public bucket alert is active (in milliseconds)
#define BLINK_INTERVAL_ALERT_MS 250

// Slow heartbeat blink interval when searching or idle (in milliseconds)
#define BLINK_INTERVAL_SAFE_MS 2000

// MQTT reconnect retry delay (in milliseconds)
#define MQTT_RECONNECT_DELAY_MS 5000

#endif // CONFIG_H
