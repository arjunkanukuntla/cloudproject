# Hardware Wiring & Pinout Guide: Cloud Security Alert Lamp

This document provides the exact pin connections, circuit schematics, and hardware specifications required to construct the physical **Cloud Security Alert Lamp** using an ESP32 microcontroller and a Red LED.

---

## 1. Components Required

| Component | Quantity | Specification / Details |
| :--- | :--- | :--- |
| **ESP32 Dev Board** | 1 | NodeMCU ESP32-WROOM-32 (30-pin or 38-pin variant) |
| **Red LED** | 1 | Standard 5mm Red LED (Forward Voltage \(\approx 1.8\text{V} - 2.0\text{V}\)) |
| **Resistor** | 1 | 220 \(\Omega\) Current Limiting Resistor (1/4W) |
| **Breadboard & Jumper Wires**| 1 | Standard solderless breadboard & Male-to-Male jumper cables |
| **Micro-USB / USB-C Cable** | 1 | Data cable for power & code flashing from PC |

---

## 2. Circuit Diagram & Schematics

### Pin Connections Table

| ESP32 Pin | Component Connection | Component Pin | Notes |
| :--- | :--- | :--- | :--- |
| **GPIO 4** | 220 \(\Omega\) Resistor | Leg 1 | Control Signal Output |
| **Resistor Leg 2** | Red LED | **Anode (+)** (Longer Leg) | Current Limiting |
| **GND** | Red LED | **Cathode (-)** (Shorter Leg / Flat Side) | Ground |
| **GPIO 2** | Onboard LED | Internal | Wi-Fi / Status Indicator |

### Schematic ASCII Diagram

```
                 ESP32 Dev Module
             +-----------------------+
             |                       |
             |  [USB Programming]    |
             |                       |
             |  [GPIO 2] ----------+ | (Internal Status LED)
             |                     | |
             |  [GPIO 4] ----+     v |
             |               |   [LED]
             |               |       |
             |  [GND] -------|---+   |
             +---------------+---|---+
                             |   |
                             v   |
                      +------------+
                      | 220 Ohm R  |
                      +------------+
                             |
                             v
                         [+] Anode  (Long Leg)
                          +---+
                          |LED| Red Alert Lamp
                          +---+
                         [-] Cathode (Short Leg)
                             |
                             +------> GND
```

---

## 3. Circuit Safety & Current Calculation

* **ESP32 Operating Voltage**: 3.3V GPIO Logic level.
* **Red LED Forward Voltage (\(V_f\))**: \(\approx 1.8\text{V}\).
* **Current Formula**:
  \[
  I = \frac{V_{GPIO} - V_f}{R} = \frac{3.3\text{V} - 1.8\text{V}}{220\,\Omega} = \frac{1.5\text{V}}{220\,\Omega} \approx 6.82\,\text{mA}
  \]
* **Safety Note**: The max recommended sink/source current per ESP32 GPIO pin is **12mA**. Outputting 6.8mA is extremely safe and ensures standard LED brightness without overloading the micro-controller.

---

## 4. Hardware Verification & Testing

1. Connect ESP32 to your PC via USB cable.
2. Ensure the longer leg (Anode) of the Red LED connects through the resistor to **GPIO 4**.
3. Ensure the shorter leg (Cathode) connects to **GND**.
4. When powered, the onboard LED on GPIO 2 will blink during Wi-Fi setup.
5. When an S3 public bucket security breach occurs, the Red LED on GPIO 4 will blink rapidly at **250ms intervals**!
