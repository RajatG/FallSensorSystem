# Fall Sensor System (IoT Firmware, KiCad PCB Hardware & Android Mobile App)

An ultra-low-power, dual-radar fall detection and room occupancy monitoring system engineered for ceiling and wall mounting with battery autonomy.

---

## 📁 Repository Overview

```
├── firmware/                        # Microcontroller & Radar Firmware
│   ├── fall_sensor_esp32_C1001_v1/  # ESP32 Firmware for C1001 60GHz Radar (v4.20)
│   ├── fall_sensor_esp32_ld2410_v1/ # ESP32 Firmware for LD2410 24GHz Radar (v4.20)
│   ├── fall_attiny_v1/              # ATtiny85 Low-Power Wake Sentinel (v4.8)
│   └── fall_attiny_mic_debug/       # ATtiny85 MIC Hardware Debug Utility
│
├── hardware/                        # KiCad 10.0 PCB & Schematic Files
│   ├── fall_sensor.kicad_sch        # Main System Schematic
│   ├── fall_sensor.kicad_pcb        # 2-Layer PCB Layout
│   ├── fall_sensor.kicad_pro        # KiCad Project Configuration
│   ├── FallSensor.kicad_sym         # Custom Symbol Library
│   ├── FallSensor.pretty/           # Custom Footprint Library
│   └── export/
│       ├── fall_sensor_gerbers.zip  # Production Gerber & Drill Package (JLCPCB/PCBWay)
│       └── pdf/                     # Printable Documentation
│           ├── fall_sensor_schematic.pdf
│           ├── fall_sensor_pcb_all_layers.pdf
│           ├── fall_sensor_pcb_top_assembly.pdf
│           └── fall_sensor_pcb_bottom_assembly.pdf
│
├── mobile_app/                      # Android Companion App (Jetpack Compose)
│   ├── app/                         # Source Code supporting C1001 & LD2410 Flavors
│   ├── build.gradle.kts
│   └── ...
│
└── docs/                            # Architectural Specs & BOM
    ├── SMD_BOM_Master_List.md       # Production SMD Component Master List
    ├── SMD_Hardware_Architecture.md # Power-path, Charger & Protection Specs
    ├── C1001_Early_Exit_Analysis.md # Radar Optimization & Timing Breakdown
    └── ATtiny85_MIC_Analysis.md     # Sentinel Threshold & Acoustic Filter Specs
```

---

## ⚡ System Architecture

### 1. Power & Wake Sentinel Architecture
- **ESP32 DevKit V1 (30-Pin)**: Deep sleep current ~10µA.
- **ATtiny85 Sentinel**: Continuously monitors AM312 PIR (Motion) and LM393 Sound Sensor (Thud/Acoustic), waking ESP32 on valid events via EXT1 wakeup pins (GPIO 13 & GPIO 4).
- **Radar Power Switching**: N-Channel MOSFET (`RADAR_MOSFET_PIN` = GPIO 27) powers radar modules only during active verification snapshot windows.
- **Smart Radar Early Exit**: Powers down radar at ~2.5s to 4.0s once occupancy is confirmed, saving up to ~90% battery energy during occupied periods.

### 2. Supported Radar Modules
| Radar | Frequency | Mounting | Fall Detection Logic | Warmup Time |
|---|---|---|---|---|
| **DFRobot C1001** | 60 GHz | Ceiling | Hardware UART fall detection (`hu.getFallData()`) | 2.5s |
| **Hi-Link LD2410** | 24 GHz | Wall | Software state machine (Motion-to-Stationary transition with 5s evaluation) | 2.5s |

### 3. Pin Mapping (ESP32 30-Pin Layout)
| Pin | Function | Description |
|---|---|---|
| **GPIO 13** | `PIR_WAKE` | ATtiny85 PB2 Wake Pulse Input |
| **GPIO 4** | `MIC_WAKE` | ATtiny85 PB0 Wake Pulse Input |
| **GPIO 25** | `PRESENCE_PIN` | Radar Presence Output / C1001 OUT1 |
| **GPIO 26** | `FALL_PIN` | Radar Fall Detection Output / C1001 OUT2 |
| **GPIO 27** | `RADAR_MOSFET_PIN` | High-side/Low-side radar power switch control |
| **GPIO 19** | `FALL_LED_PIN` | Visual Alert LED / Flashing Siren |
| **GPIO 33** | `SYNC_BUTTON_PIN` | Manual Sync & Alarm Clear Button |
| **GPIO 34** | `BATTERY_PIN` | ADC Battery Voltage Sensing (100k/100k divider) |
| **GPIO 16** | `RX_PIN` | Radar UART RX (connects to Radar TX) |
| **GPIO 17** | `TX_PIN` | Radar UART TX (connects to Radar RX) |

---

## 📱 Mobile App Features
- **Jetpack Compose Native UI**: Modern dark theme with animated status cards and real-time glow indicators.
- **Multi-Sensor Flavors**: Build variants for both `c1001` and `ld2410` devices with automatic BLE advertising prefix targeting.
- **Battery Health & Autonomy Prediction**: Tracks voltage discharge curves over time to forecast remaining battery days.
- **Live Diagnostics & Settings**:
  - Live Uptime Counter (`Xh Ym Zs`).
  - Configurable Battery Warning Thresholds & Capacity (mAh).
  - 5-second auto-clearing LED pulse timers for acoustic & PIR triggers.
  - Non-intrusive logging (suppresses high-frequency radar UART streams unless `LOG_ON` is enabled).

---

## 🛠️ Manufacturing & Assembly

- **Gerber Package**: Located at [`hardware/export/fall_sensor_gerbers.zip`](hardware/export/fall_sensor_gerbers.zip). Ready for upload directly to JLCPCB, PCBWay, or OSH Park.
- **Schematic PDF**: [`hardware/export/pdf/fall_sensor_schematic.pdf`](hardware/export/pdf/fall_sensor_schematic.pdf).
- **PCB Layout PDFs**: Multi-page and individual layer PDFs located in [`hardware/export/pdf/`](hardware/export/pdf/).
