# 📋 Fall Sensor System — Master 4-Stream Completion Roadmap & Engineering Recommendations

> **Repository:** [RajatG/FallSensorSystem](https://github.com/RajatG/FallSensorSystem)  
> **Last Updated:** September 2026  
> **System Architecture:** Low-Power Dual Radar (C1001 60GHz / LD2410 24GHz) + ATtiny85 Sentinel + ESP32 Main MCU + Android App + 3D Enclosure

---

## 🎯 Executive Dashboard: 4 Engineering Streams

| Stream | Status | Completion | Milestone Reached | Next Steps / Roadmap |
|---|---|:---:|---|---|
| **1. Firmware / Software** | ✅ Verified | **95%** | v4.23 Silent Fall (Gradual Posture Collapse) logic implemented in both C1001 & LD2410 | Configurable floor threshold slider in app, auto acoustic threshold calibration |
| **2. Hardware (PCB Rev A)** | ✅ DRC Clean | **92%** | Full 100×80mm 2-layer CAD, 0 errors, 0 unconnected nets, 1:1 true scale PDFs, Gerbers packaged | Production SMD Migration (Rev B) |
| **3. 3D Enclosure (v2.0)** | ✅ Complete | **100%** | Modern Square profile ($106.8 \times 110.8 \times 31.4\text{ mm}$), integrated 18650 bay, left-wall USB-C port, high-res renders | Ready for slicer / 3D printing (PETG/ABS) |
| **4. Mobile App (Android)** | ✅ Functional | **92%** | Jetpack Compose dark UI, C1001 & LD2410 build flavors, BLE telemetry parser, lifetime prediction | High-priority audible alarm channel, floor threshold slider |

---

## 1. 🖥️ Firmware Stream: Progress & Next Steps

### Implemented Capabilities
- **Dual Radar Support:** Independent optimized firmware for DFRobot C1001 60GHz (Ceiling mount) and Hi-Link LD2410 24GHz (Wall mount).
- **ATtiny85 Wake Sentinel:** Hardware interrupt wake-on-motion (AM312 PIR) and wake-on-acoustic impact (LM393 sound module).
- **Smart Radar Early Exit:** Powers down radar at 2.5s–4.0s once occupancy is confirmed, cutting active battery consumption by ~90%.
- **Gradual Posture Collapse Detection (Silent Fall Fix - v4.23):** Tracks standing-to-floor transitions over a 30s sliding window in RTC memory to catch slow collapses (fainting, slipping from a chair) without waiting 120s for periodic scans.

### Recommended Next Firmware Steps
1. **Configurable Floor Lying Threshold:** Expose `FLOOR_LYING_ALERT_THRESHOLD` via BLE command `SET:FLOOR_THRESHOLD:<n>` so caregivers can adjust sensitivity between hospital and home settings.
2. **Acoustic Background Auto-Calibration:** Implement `CALIBRATE_MIC` command to sample 10 seconds of ambient acoustic room noise and set the software trigger baseline dynamically.
3. **BLE Encryption / Passkey Pairing:** Add secure passkey bonding to prevent unauthorized local BLE disarm.

---

## 2. 🔌 Hardware Stream & SMD Production Migration (Rev B)

### Current Rev A (Prototype)
- **Form Factor:** $100.00 \times 80.00\text{ mm}$ 2-layer FR4 PCB ($1.6\text{ mm}$ thickness, 1 oz copper).
- **Construction:** Modular breakout socketing using commercially available off-the-shelf boards (ESP32 DevKit V1, Digispark ATtiny85, TP4056, MT3608, LM393, AM312, C1001, DBVT load switch).
- **Verification:** 0 DRC Errors, 0 Unconnected Nets. Gerber production package ready in [`hardware/export/fall_sensor_gerbers.zip`](../hardware/export/fall_sensor_gerbers.zip).

### 🚀 Production SMD Migration Roadmap (Rev B)
Moving from breakout modules to a single, high-reliability commercial SMD board:

| Prototype Breakout | → Production SMD Component | Package | Key Benefit |
|---|---|---|---|
| **ESP32 DevKit V1 (30-pin)** | **ESP32-WROOM-32E-N4** | SMD Module ($18 \times 25.5\text{ mm}$) | Pre-certified FCC/CE RF shield, integrated antenna, eliminates 30 THT header pins |
| **Digispark ATtiny85** | **ATtiny85-20SU** | SOIC-8 ($5 \times 4\text{ mm}$) | Ultra-low standby current ($< 1\mu\text{A}$), solder directly to PCB |
| **TP4056 Charger Breakout** | **TP4056 IC** + passives | ESOP-8 ($4.9 \times 3.9\text{ mm}$) | Direct onboard thermal pad charging up to 1A |
| **MT3608 Boost Breakout** | **MT3608 IC** + 22µH SMT inductor | SOT-23-6 ($2.9 \times 1.6\text{ mm}$) | Compact high-frequency 1.2MHz boost converter |
| **LM393 Sound Breakout** | **LM393G** + SMT electret mic | SOIC-8 + 4mm SMT Mic | Direct audio comparator with onboard trimpot or fixed divider |
| **AM312 PIR Breakout** | **AS312 / BISS0001** sensor | SOT-23-6 / TO-5 | Low-profile SMD PIR sensor element with integrated lens ring |
| **Through-Hole Passives** | **0805 / 0603 SMD Resistors & Caps** | 0805 / 0603 | Mass-production pick-and-place compatibility |
| **Load Switch Socket** | **TPS22918DBVT** | SOT-23-6 | Native PCB footprint (no daughterboard adapter needed) |
| **Slide Switch** | **SS-12D00 SMT** | SMT 3-Pin | Low-profile side-actuated surface mount slide switch |
| **Sync Button** | **EVQ-P7A01K / TS-1187** | SMT 4-Pin | $3 \times 4\text{ mm}$ tactile button |

### Essential Protection Circuitry for Rev B SMD
1. **Battery Protection IC (DW01A + FS8205A dual N-MOSFET):** Built-in over-charge (4.3V), over-discharge (2.4V), and over-current protection.
2. **USB-C ESD Protection (USBLC6-2SC6):** 15kV electrostatic discharge protection array on CC1, CC2, and VBUS lines.
3. **Reverse Polarity Protection (AO3401A P-Channel MOSFET):** Prevents board damage if battery polarity is accidentally reversed.
4. **Integrated Power-Path PMIC Option (BQ24075 or IP5306):** Allows the system to run directly from USB-C wall power while simultaneously recharging the 18650 cell with seamless zero-dropout switchover.
5. **NTC Thermistor (10k 3950):** Connects to charger TEMP pin to halt charging below 0°C or above 45°C for lithium safety.

---

## 3. 📦 3D Enclosure Stream (v2.0 Square)

### Final Specifications
- **Dimensions:** $106.8\text{ mm (Width)} \times 110.8\text{ mm (Depth)} \times 31.4\text{ mm (Total Height)}$ (Aspect ratio `0.96 : 1` square).
- **Integrated Battery Compartment:** Dedicated top bay ($102 \times 22\text{ mm}$) separated from the PCB by a $2.0\text{ mm}$ thermal divider wall with an $8 \times 6\text{ mm}$ wire notch routing directly to `BT1`.
- **Wall Mounting:** Dual rear keyholes spaced $50.0\text{ mm}$ apart for secure slide-and-lock wall attachment.
- **Port Alignment:**
  - **Left Wall:** TP4056 USB-C charging slot ($11.0 \times 4.8\text{ mm}$) and Power Switch slot ($9.5 \times 5.0\text{ mm}$) separated by a solid $5.2\text{ mm}$ structural bridge.
  - **Front Face:** PIR Fresnel dome aperture ($\varnothing 12\text{ mm}$), Microphone acoustic port ($\varnothing 3\text{ mm}$), Alarm LED hole ($\varnothing 3.2\text{ mm}$), Sync pinhole ($\varnothing 3.5\text{ mm}$), and internal $1.0\text{ mm}$ thin-wall RF transmission window for the C1001 mmWave radar.
- **Fabrication Assets:** Watertight binary STLs [`fall_sensor_enclosure_base.stl`](../enclosure/fall_sensor_enclosure_base.stl) and [`fall_sensor_enclosure_lid.stl`](../enclosure/fall_sensor_enclosure_lid.stl) ready for slicer.

---

## 4. 📱 Mobile App Stream: Android Companion

### Implemented Features
- **Architecture:** 100% Kotlin + Jetpack Compose + Material 3 Dark Theme.
- **Telemetry Parsing:** Live voltage, battery life prediction in days, radar distance (cm), occupancy status, fall status, and event counters.
- **Sensor Flavors:** Separate Gradle product flavors for `c1001` (Ceiling) and `ld2410` (Wall) devices.

### Recommended Next App Steps
1. **High-Priority Fall Alarm Notification:** Create an Android high-importance notification channel that plays an audible siren sound and triggers vibration when `ALERT: FALL DETECTED` is received, even if the app is in the background or the screen is locked.
2. **Caregiver SMS / Webhook Dispatch:** Add an option in the app to auto-dispatch an SMS alert or HTTP webhook (e.g. Home Assistant, Telegram, Twilio) when a confirmed fall event occurs.
3. **Historical Event Log:** Persist timestamped fall events and battery discharge curves to a local Room SQLite database.
