# Fall Sensor System (IoT Firmware, KiCad PCB Hardware & Android Mobile App)

An ultra-low-power, dual-radar fall detection and room occupancy monitoring system engineered for ceiling and wall mounting with battery autonomy.

---

## 📁 Repository Overview

```
├── firmware/                        # Microcontroller & Radar Firmware
│   ├── fall_sensor_esp32_C1001_v1/  # ESP32 Firmware for C1001 60GHz Radar (v4.23)
│   ├── fall_sensor_esp32_ld2410_v1/ # ESP32 Firmware for LD2410 24GHz Radar (v4.23)
│   ├── fall_attiny_v1/              # ATtiny85 Low-Power Wake Sentinel (v4.8)
│   └── fall_attiny_mic_debug/       # ATtiny85 MIC Hardware Debug Utility
│
├── hardware/                        # KiCad 10.0 PCB & Schematic Files
│   ├── fall_sensor.kicad_sch        # Main System Schematic
│   ├── fall_sensor.kicad_pcb        # 2-Layer PCB Layout
│   ├── fall_sensor.kicad_pro        # KiCad Project Configuration
│   ├── FallSensor.kicad_sym     # Custom Symbol Library
│   ├── FallSensor.pretty/       # Custom Footprint Library
│   └── export/
│       ├── fall_sensor_gerbers.zip  # Production Gerber & Drill Package (JLCPCB/PCBWay)
│       └── pdf/                     # Printable Documentation (See hardware/export/pdf/README.md)
│           ├── fall_sensor_pcb_front_and_back_A4.pdf  # 1:1 True Scale Paper Testing Sheet
│           ├── fall_sensor_schematic_A4_printable.pdf # Printable A4 Schematic
│           ├── assembly/            # Top & Bottom Assembly Drawings
│           ├── layers/              # Top & Bottom Copper Layer Plots
│           └── schematic/           # Full-Size A3 Engineering Schematic
│
├── enclosure/                       # 3D Printed Wall-Mount Enclosure (v2.1 Square)
│   ├── fall_sensor_enclosure_base.stl # Base Mount with 18650 Battery Bay & PCB Standoffs
│   ├── fall_sensor_enclosure_lid.stl  # Front Cover with Apertures & Alignment Lip
│   ├── build_square_enclosure.py      # Parametric Blender Python CAD Script (v2.1)
│   ├── fall_sensor_enclosure.blend    # Master Blender CAD Project & Studio Renders
│   └── README.md                      # Mechanical Specifications & Slicer Guide
│
├── mobile_app/                      # Android Companion App (Jetpack Compose)
│   ├── app/                         # Source Code supporting C1001 & LD2410 Flavors
│   ├── build.gradle.kts
│   └── ...
│
└── docs/                            # Architectural Specs, Roadmaps & Engineering Docs (See docs/README.md)
    ├── README.md                    # Master Documentation Hub & Flow Map
    ├── Firmware_Architecture_and_Detection_Logic.md  # Complete Firmware Logic & 4-Layer Fall Pipeline
    ├── Master_4Stream_Roadmap_and_Recommendations.md # Comprehensive 4-Stream Status & Production Roadmap
    ├── PCB_Component_Connections_Verification.md     # Master 21-Component Netlist & Pinout Verification Guide
    ├── PCB_Component_Footprints_and_Dimensions.md    # Physical Dimensions, Drills & Pad Pitch Reference
    ├── SMD_BOM_Master_List.md       # Production SMD Component Master List (Rev B)
    ├── SMD_Hardware_Architecture.md # Power-path, Charger & Protection Circuitry Specs
    ├── C1001_Early_Exit_Analysis.md # Radar Optimization & Timing Breakdown
    └── ATtiny85_MIC_Analysis.md     # Sentinel Threshold & Acoustic Filter Specs
```

---

## ⚡ System Overview & Architecture

### What the System Is
The **Fall Sensor System** is a privacy-first, contactless room occupancy and fall detection device designed for elder care and clinical environments. It eliminates the need for cameras, audio-recording microphones, or wearable pendants.

### How it Works: The Staged-Wakeup Architecture
Operating mmWave radar continuously requires 60–120 mA, which would exhaust a battery in under two days. To achieve long battery life on a single 18650 cell, the system uses an **asymmetric staged-wakeup architecture**:

```
+-----------------------------------------------------------------------------------+
| 1. PASSIVE SENSING (Continuous ~35uA Draw)                                        |
|    - AM312 PIR watches for motion cone entry.                                     |
|    - LM393 acoustic sensor watches for mechanical floor impact shockwaves.       |
|    - ATtiny85 Sentinel debounces signals while ESP32 and Radar sleep.             |
+-----------------------------------------+-----------------------------------------+
                                          | Valid Motion or Thud Pulse
                                          v
+-----------------------------------------------------------------------------------+
| 2. RADAR VERIFICATION SNAPSHOT (2.5s - 4.0s Window)                               |
|    - ESP32 wakes from deep sleep and gates Radar power via MOSFET switch.         |
|    - mmWave Radar measures distance, target velocity, and floor-level coordinates.|
+-----------------------------------------+-----------------------------------------+
                                          |
                      +-------------------+-------------------+
                      |                                       |
              [ Normal Upright Motion ]               [ Confirmed Fall ]
                      |                                       |
                      v                                       v
+---------------------------------------------+ +-----------------------------------+
| 3. SMART EARLY EXIT                         | | 4. IMMEDIATE ALERTING             |
|    - Target confirmed standing/walking.     | |    - Red Fall Siren LED activates.|
|    - Radar cuts power at 2.5s - 4.0s.       | |    - BLE alert packet transmitted |
|    - BLE occupancy status updated.          | |      to Android caregiver app.    |
|    - ESP32 returns to deep sleep (<15uA).   | |    - Persists until recovery or   |
|      (Saves ~90% energy per event)          | |      manual sync button reset.    |
+---------------------------------------------+ +-----------------------------------+
```

---

## 📦 Engineering Streams & Subunit Documentation

The system is organized into four self-contained, documented engineering streams:

| Stream | Subunit Directory | Key Deliverables & Documentation |
|---|---|---|
| **⚡ Firmware** | [`firmware/`](firmware/README.md) | ESP32 C1001 & LD2410 drivers, ATtiny85 wake sentinel, v4.23 Gradual Posture Collapse detection, and flashing guides. |
| **🔌 Hardware (PCB)** | [`hardware/`](hardware/README.md) | KiCad 10.0 schematics, 2-layer PCB ($100 \times 80\text{ mm}$), pin mapping table, Gerbers, and 1:1 scale printable test sheets. |
| **🖨️ 3D Enclosure** | [`enclosure/`](enclosure/README.md) | v2.1 Square CAD model ($116.8 \times 110.8 \times 31.4\text{ mm}$), 18650 battery cradle, STL meshes, slicer settings, and photorealistic renders. |
| **📱 Mobile App** | [`mobile_app/`](mobile_app/README.md) | Android companion application (Jetpack Compose, Kotlin, BLE GATT), telemetry parser, and build flavor instructions. |
| **📚 Documentation** | [`docs/`](docs/README.md) | Master documentation hub, 4-layer fall logic specification, radar early exit analysis, acoustic sensitivity analysis, and SMD Rev B migration roadmap. |

---

## 🚀 Quick Manufacturing & Test Links

* **PCB Fabrication Gerbers:** [`hardware/export/fall_sensor_gerbers.zip`](hardware/export/fall_sensor_gerbers.zip) (Ready for JLCPCB/PCBWay upload).
* **1:1 Scale Paper Test Sheet:** [`hardware/export/pdf/fall_sensor_pcb_front_and_back_A4.pdf`](hardware/export/pdf/fall_sensor_pcb_front_and_back_A4.pdf) (For physical component fitting).
* **3D Printable STLs:** [`enclosure/fall_sensor_enclosure_base.stl`](enclosure/fall_sensor_enclosure_base.stl) and [`enclosure/fall_sensor_enclosure_lid.stl`](enclosure/fall_sensor_enclosure_lid.stl).

