# 🧠 Fall Sensor System — Complete Firmware Architecture & Fall Detection Logic

> **Authoritative Technical Specification**  
> **Firmware Versions:** ESP32 C1001 v4.23 | ESP32 LD2410 v4.23 | ATtiny85 Sentinel v4.8  
> **Repository:** [RajatG/FallSensorSystem](https://github.com/RajatG/FallSensorSystem)

---

## 🧭 Document Navigation & Cross-References

This document serves as the master guide for the firmware execution flow. Detailed sub-investigations and hardware analyses are linked directly:
* ⚡ **Radar Snapshot & Early Exit Optimization:** See [`C1001_Early_Exit_Analysis.md`](C1001_Early_Exit_Analysis.md) for UART loop timing and power optimization.
* 🎙️ **Acoustic Thud Thresholds & Sentinel Wakeup:** See [`ATtiny85_MIC_Analysis.md`](ATtiny85_MIC_Analysis.md) for LM393 voltage level matching and ATtiny85 interrupt timing.
* 📋 **Production Roadmap & SMD Migration:** See [`Master_4Stream_Roadmap_and_Recommendations.md`](Master_4Stream_Roadmap_and_Recommendations.md).
* 🔌 **Hardware Pinout & Net Connections:** See [`PCB_Component_Connections_Verification.md`](PCB_Component_Connections_Verification.md).

---

## 1. 🏗️ High-Level System Architecture & State Machine

The Fall Sensor System uses a **hybrid asymmetric dual-processor architecture** to achieve years of battery autonomy while providing sub-second fall detection:

```
                      +-----------------------------+
                      |   AM312 PIR (Motion)        |
                      +--------------+--------------+
                                     |
                      +--------------v--------------+
                      |  LM393 Mic (Acoustic Thud)  |
                      +--------------+--------------+
                                     |
             Continuous 30uA         v
         +-------------------------------------------------------+
         |      ATtiny85 Ultra-Low-Power Wake Sentinel           |
         |  - Evaluates analog/digital pulses                    |
         |  - Filters acoustic noise and PIR settling times      |
         +-------------------+-------------------------------+
                             |
                   Wake Pulse (PB0 / PB2)
                             |
                             v
         +-------------------------------------------------------+
         |     ESP32 DevKit V1 (Main Controller - Deep Sleep)    |
         |  - Wakes via EXT1 interrupt on GPIO 13 or GPIO 4      |
         |  - Switches ON Radar via Load Switch (GPIO 27)        |
         |  - Performs 2.5s-4.0s Target Verification Snapshot    |
         |  - Analyzes Multi-Layer Fall Pipeline                 |
         |  - Dispatches BLE Telemetry / Alarm to Android App   |
         |  - Returns to Deep Sleep (< 15uA)                     |
         +-------------------------------------------------------+
```

---

## 2. 💤 Power States & Deep Sleep Cycle

1. **Deep Sleep State (Default):**
   * ESP32 CPU is powered down; RTC controller remains active. Total current: **~10–15 µA**.
   * C1001 / LD2410 Radar power is cut via N-channel MOSFET / SOT-23-6 load switch (`RADAR_MOSFET_PIN` = GPIO 27). Current: **0 µA**.
   * ATtiny85 Sentinel runs continuously in `SLEEP_MODE_PWR_DOWN`, waking on pin-change interrupts from the AM312 PIR (`P1`) or LM393 Sound Sensor (`P4`). Current: **~25–35 µA**.
   * Total system baseline idle draw: **$< 50\ \mu\text{A}$** (permitting months of operation on a single 18650 cell).

2. **Wakeup Sources (`esp_sleep_get_wakeup_cause()`):**
   * **`ESP_SLEEP_WAKEUP_EXT1`:**
     * `GPIO 13` HIGH: Motion detected by PIR (Sentinel generated a 50 ms pulse on PB2).
     * `GPIO 4` HIGH: Sudden acoustic impact/thud detected by Microphone (Sentinel generated a 50 ms pulse on PB0).
   * **`ESP_SLEEP_WAKEUP_TIMER`:** Periodic watchdog heartbeat wake every 60 seconds to inspect battery voltage and check room presence.
   * **Manual Sync Button (`GPIO 33`):** Wakes system for BLE pairing and clears active alarm flags.

---

## 3. ⚡ Radar Power Switching & Early Exit Logic

When the ESP32 wakes:
1. It pulls `RADAR_MOSFET_PIN` (GPIO 27) **HIGH** to energize the radar module.
2. **Warmup Window:** Both the C1001 (60 GHz) and LD2410 (24 GHz) require **2.5 seconds** for their internal DSP filters to stabilize.
3. **Smart Early Exit (Power Optimization):**
   * *Problem:* Running a full 30-second radar snapshot every time a person walks by drains battery rapidly.
   * *Solution:* As detailed in [`C1001_Early_Exit_Analysis.md`](C1001_Early_Exit_Analysis.md), once the 2.5s warmup completes, the firmware checks `isOccupiedNow`:
     * If a standing, moving human is verified at normal height ($> 50\text{ cm}$ above floor) and **NO fall flag** is asserted:
     * The ESP32 dispatches a single BLE occupancy status update and **powers down the radar immediately at $t = 2.5\text{s} - 4.0\text{s}$**, returning to deep sleep!
     * Energy savings: **Up to 88–92% reduction** in active radar consumption during occupied room states.

---

## 4. 🚨 Multi-Layer Fall Detection Pipeline

To prevent false alarms from dropped objects while guaranteeing no real fall is missed, the firmware uses a **4-layer progressive verification pipeline**:

```
+-----------------------------------------------------------------------------------+
| LAYER 1: Acoustic Impact Detection (LM393 + ATtiny85)                             |
| Triggers when a mechanical impact wave strikes the floor.                         |
| Detailed in: ATtiny85_MIC_Analysis.md                                             |
+-----------------------------------------+-----------------------------------------+
                                          |
+-----------------------------------------v-----------------------------------------+
| LAYER 2: Radar Dynamic Velocity Fall Flag (C1001 / LD2410)                        |
| Hardware UART/GPIO signal asserted when rapid downward descent velocity occurs.   |
+-----------------------------------------+-----------------------------------------+
                                          |
+-----------------------------------------v-----------------------------------------+
| LAYER 3: Static Floor-Level Distance Verification                                 |
| Verifies if human presence target distance >= (roomHeightCm - floorToleranceCm).  |
+-----------------------------------------+-----------------------------------------+
                                          |
+-----------------------------------------v-----------------------------------------+
| LAYER 4: Gradual Posture Collapse Detection (Silent Fall Fix - v4.23)             |
| Tracks standing-to-floor transition time (< 30s) in RTC non-volatile memory.      |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
                      [ CONFIRMED FALL ALARM DISPATCHED ]
```

### Layer Details:

* **Layer 1: Acoustic Impact (LM393):**
  A body hitting the floor generates a low-frequency shockwave. The LM393 comparator pulls `DO` HIGH, which the ATtiny85 debounces and relays to ESP32 GPIO 4. *(Note: As documented in [`ATtiny85_MIC_Analysis.md`](ATtiny85_MIC_Analysis.md), proper $V_{IH}$ logic level matching is required).*

* **Layer 2: Radar Dynamic Fall Flag:**
  * **C1001 (60 GHz):** Hardware UART returns fall state (`hu.getFallData(hu.eFallState) == 1 || 2`) or OUT2 GPIO 26 asserts HIGH.
  * **LD2410 (24 GHz):** Software state machine tracks transition from high-energy moving gates to low-energy stationary floor gate.

* **Layer 3: Static Floor-Level Distance Verification:**
  Default ceiling height is **9.0 feet ($274\text{ cm}$)**.
  ```cpp
  bool isAtFloorLevel = (presenceDetected && dist >= (roomHeightCm - floorToleranceCm));
  ```
  If distance measurement places target within 45 cm of the floor, floor-level lying is flagged.

* **Layer 4: Gradual Posture Collapse (The "Silent Fall" Fix - v4.23):**
  * *The Edge Case:* If a person slowly faints or slides down from a chair, there is **no acoustic thud (Layer 1 fails)** and **no high-velocity downward spike (Layer 2 fails)**.
  * *v4.23 Fix:* The firmware stores `lastStandingDistCm` and `lastStandingTime` in RTC persistent memory. If the target transitions from standing ($< 150\text{ cm}$) to floor ($> 230\text{ cm}$) in **$< 30\text{ seconds}$**, an immediate fall alert is confirmed without waiting for multi-minute periodic verification timers:
    ```cpp
    if (isAtFloorLevel && lastStandingDistCm > 0 && lastStandingTime > 0) {
        unsigned long transitionTime = millis() - lastStandingTime;
        if (transitionTime > 0 && transitionTime < 30000) {
            fallConfirmed = true;
            sendBLENotification("ALERT: FALL DETECTED (Gradual Posture Collapse)!\n");
        }
    }
    ```

---

## 5. 🔄 Fall Alarm Clearance & Recovery

A confirmed fall alarm remains active until one of two conditions occurs:
1. **Sustained Recovery Movement:** The radar detects the person has stood back up into the standing zone ($dist < roomHeight - 45\text{ cm}$) continuously for $> 5\text{ seconds}$.
2. **Manual Dismissal:** Caregiver presses the physical Sync Button (`SW1` on GPIO 33) or sends the `RESET` command via the Android mobile app.

---

## 6. 📡 Bluetooth Low Energy (BLE) Telemetry & Protocol

* **Device Name Prefix:** `FallSensor_C1001` or `FallSensor_LD2410`
* **GATT Service UUID:** `4fafc201-1fb5-459e-8fcc-c5c9c331914b`
* **Characteristic UUID:** `beb5483e-36e1-4688-b7f5-ea07361b26a8`

### Command Set (App $\rightarrow$ ESP32):
| Command | Action |
|---|---|
| `LOG_ON` | Enables live 100ms radar distance and gate streaming to BLE console |
| `LOG_OFF` | Disables verbose logging to conserve BLE bandwidth and power |
| `SET:HEIGHT:<cm>` | Reconfigures room ceiling height in non-volatile flash (e.g. `SET:HEIGHT:274`) |
| `RESET` | Clears active fall alarm and resets posture tracking state |
| `OTA_ON` | Enables ArduinoOTA network flash mode |

### Telemetry Packet Format (ESP32 $\rightarrow$ App):
```
STATUS: BATT=4.12V, STATE=OCCUPIED, DIST=185cm, FALL=0, PIR=1, MIC=0, UPTIME=01h 22m 14s
```
If a fall occurs:
```
ALERT: FALL DETECTED (Impact + Radar Verified at 268cm)!
```
or
```
ALERT: FALL DETECTED (Gradual Posture Collapse in 14s)!
```
