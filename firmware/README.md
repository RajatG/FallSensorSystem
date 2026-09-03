# ⚡ Microcontroller & Sensor Firmware

This directory contains the production firmware for the dual-processor fall detection pipeline, supporting both 60GHz ceiling-mounted and 24GHz wall-mounted radar variants.

---

## 📁 Firmware Modules

| Directory | Target Hardware | Role | Core Functions |
|---|---|---|---|
| **[`fall_sensor_esp32_C1001_v1/`](fall_sensor_esp32_C1001_v1/)** | ESP32 DevKit V1 (30-pin) | Main Controller (Ceiling) | C1001 60GHz UART radar driver, 2.5s warmup, smart early exit, 4-layer fall detection (including v4.23 Gradual Posture Collapse), BLE GATT telemetry server, deep sleep management. |
| **[`fall_sensor_esp32_ld2410_v1/`](fall_sensor_esp32_ld2410_v1/)** | ESP32 DevKit V1 (30-pin) | Main Controller (Wall) | Hi-Link LD2410 24GHz radar driver, moving/stationary gate state machine, BLE GATT server, deep sleep management. |
| **[`fall_attiny_v1/`](fall_attiny_v1/)** | ATtiny85 (Digispark) | Ultra-Low-Power Sentinel | Continuous ~30µA motion/acoustic monitor. Debounces AM312 PIR and LM393 sound detector, generating 50ms wake pulses to ESP32 EXT1 pins. |
| **[`fall_attiny_mic_debug/`](fall_attiny_mic_debug/)** | ATtiny85 (Digispark) | Hardware Diagnostic Tool | Diagnostic utility with onboard LED blink codes to verify acoustic comparator logic levels ($V_{IH}$) on PB4. |

---

## ⚙️ Compilation & Flashing Instructions

### 1. ESP32 Firmware (`C1001` or `LD2410`)
* **Environment:** Arduino IDE 2.x or PlatformIO
* **Board:** `DOIT ESP32 DEVKIT V1`
* **Partition Scheme:** `Default 4MB with spiffs (1.2MB APP / 1.5MB SPIFFS)`
* **Dependencies:**
  * `DFRobot_HumanDetection` (for C1001)
  * `LD2410` by ncmreynolds (for LD2410)
  * Standard ESP32 core libraries (`BLEDevice`, `BLEServer`, `BLEUtils`, `BLE2902`, `WiFi`, `ArduinoOTA`)
* **Flash Settings:** Upload Speed: `921600`, Flash Frequency: `80MHz`.

### 2. ATtiny85 Sentinel Firmware
* **Environment:** Arduino IDE 2.x with `ATTinyCore` by SpenceKonde
* **Board:** `ATtiny85 (Micronucleus / Digispark)`
* **Clock Source:** `1 MHz (Internal)` — *Ensures minimum active current draw ($< 250\mu\text{A}$ active, $< 5\mu\text{A}$ deep sleep)*.
* **Upload:** Plug Digispark into USB only when prompted by the Micronucleus uploader.

---

## 📖 In-Depth Technical References
* Detailed state machines, timing diagrams, and fall algorithms: [`../docs/Firmware_Architecture_and_Detection_Logic.md`](../docs/Firmware_Architecture_and_Detection_Logic.md)
* C1001 Radar UART optimization and early exit benchmarks: [`../docs/C1001_Early_Exit_Analysis.md`](../docs/C1001_Early_Exit_Analysis.md)
* ATtiny85 acoustic comparator voltage thresholds: [`../docs/ATtiny85_MIC_Analysis.md`](../docs/ATtiny85_MIC_Analysis.md)
