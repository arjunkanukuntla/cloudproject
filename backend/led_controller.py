"""
Physical Security Alert Lamp - Desktop / IoT Device Controller.
Can run on:
1. Raspberry Pi (using physical GPIO pins)
2. Desktop PC (Windows / Linux / macOS) with interactive terminal/desktop visualizer
3. Connected to AWS IoT Core MQTT or Local Backend WebSocket/REST

Subscribes to MQTT topic: 'cloud/security/alerts' or 'security/alert/led'
"""

import os
import sys
import time
import json
import logging
import threading
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [LED_CONTROLLER] %(message)s"
)
logger = logging.getLogger("led_controller")

# Configuration
AWS_IOT_ENDPOINT = os.getenv("AWS_IOT_ENDPOINT", "")
TOPIC = os.getenv("AWS_IOT_TOPIC", "cloud/security/alerts")
BACKEND_WS_URL = os.getenv("BACKEND_WS_URL", "ws://localhost:8000/ws")
LED_PIN = int(os.getenv("LED_PIN", "4"))

# Detect Raspberry Pi Hardware
IS_RASPBERRY_PI = False
gpio = None
try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.output(LED_PIN, GPIO.LOW)
    gpio = GPIO
    IS_RASPBERRY_PI = True
    logger.info(f"Hardware Detected: Raspberry Pi (GPIO Pin {LED_PIN})")
except (ImportError, RuntimeError):
    logger.info("Hardware: Standard Computer / Simulation Mode (Virtual Lamp Visualizer active)")

class PhysicalSecurityLamp:
    def __init__(self):
        self.state = "OFF"
        self.running = True
        self.blinking_thread = None
        self.lock = threading.Lock()

    def set_led_physical(self, on: bool):
        if IS_RASPBERRY_PI and gpio:
            gpio.output(LED_PIN, GPIO.HIGH if on else GPIO.LOW)

    def _blink_loop(self):
        """Worker thread to blink LED continuously when in alert state."""
        logger.info("🔴 >>> BLINK THREAD STARTED: Lamp is actively blinking! <<<")
        is_lit = False
        while True:
            with self.lock:
                if self.state != "BLINKING" or not self.running:
                    break
            is_lit = not is_lit
            self.set_led_physical(is_lit)
            
            # Visual ASCII simulation in terminal
            indicator = "🚨 [🔴 RED LED: *** FLASHING ALERT ***]" if is_lit else "   [⚫ RED LED: --- DARK PAUSE ---]"
            print(f"\r{indicator}  (Press Ctrl+C to exit)", end="", flush=True)
            time.sleep(0.3)
            
        self.set_led_physical(False)
        print("\r                                                                \r", end="", flush=True)
        logger.info("⚪ >>> BLINK THREAD STOPPED: Lamp turned OFF. <<<")

    def apply_state(self, new_state: str, reason: str = ""):
        with self.lock:
            old_state = self.state
            self.state = new_state.upper()

        if self.state in ("BLINKING", "ALERT"):
            logger.warning(f"⚠️ SECURITY ALERT RECEIVED: Reason: '{reason}' -> ACTIVATING RED LED BLINK")
            if old_state not in ("BLINKING", "ALERT"):
                self.state = "BLINKING"
                self.blinking_thread = threading.Thread(target=self._blink_loop, daemon=True)
                self.blinking_thread.start()
        else:
            logger.info(f"✅ SYSTEM SECURE RECEIVED: Reason: '{reason}' -> TURNING LED OFF")
            self.set_led_physical(False)

    def shutdown(self):
        self.running = False
        self.apply_state("OFF")
        if IS_RASPBERRY_PI and gpio:
            gpio.cleanup()

lamp = PhysicalSecurityLamp()

def handle_message(payload_str: str):
    """Processes incoming MQTT / WebSocket payload."""
    try:
        data = json.loads(payload_str)
        status = data.get("status") or data.get("led")
        count = data.get("public_buckets_count", 0)
        
        if status == "ALERT" or count > 0:
            lamp.apply_state("BLINKING", f"Exposed Buckets Count: {count}")
        else:
            lamp.apply_state("OFF", "System Secure")
    except Exception as e:
        logger.error(f"Error parsing incoming message: {e}")

def run_websocket_listener():
    """Connects to FastAPI backend WebSocket to receive real-time LED triggers."""
    import asyncio
    import websockets

    async def ws_loop():
        uri = BACKEND_WS_URL
        logger.info(f"Connecting to Cloud Security Lamp Backend WebSocket at {uri}...")
        while True:
            try:
                async with websockets.connect(uri) as websocket:
                    logger.info("Connected to Backend WebSocket! Listening for real-time LED alerts...")
                    async for message in websocket:
                        handle_message(message)
            except Exception as e:
                logger.warning(f"WebSocket connection retry in 3 seconds: {e}")
                await asyncio.sleep(3)

    try:
        asyncio.run(ws_loop())
    except KeyboardInterrupt:
        pass

def main():
    print("=" * 60)
    print("   CLOUD SECURITY ALERT LAMP - IOT DEVICE CONTROLLER   ")
    print("=" * 60)
    print(f"Device Mode   : {'Raspberry Pi (Hardware GPIO)' if IS_RASPBERRY_PI else 'Desktop / Terminal Simulator'}")
    print(f"MQTT Topic    : {TOPIC}")
    print(f"Initial State : OFF (System Secure)")
    print("Listening for AWS IoT / Backend alerts...")
    print("=" * 60)

    try:
        run_websocket_listener()
    except KeyboardInterrupt:
        logger.info("Shutting down controller...")
    finally:
        lamp.shutdown()

if __name__ == "__main__":
    main()
