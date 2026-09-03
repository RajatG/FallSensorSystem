# 🔌 Hardware CAD & PCB Engineering (KiCad 10.0)

This directory contains the complete electronic schematic and PCB design files for the Fall Sensor System prototype (Rev A).

---

## 📁 Hardware Files

| File / Folder | Type | Description |
|---|:---:|---|
| **[`fall_sensor.kicad_sch`](fall_sensor.kicad_sch)** | Schematic | Main system schematic in KiCad 10 format. |
| **[`fall_sensor.kicad_pcb`](fall_sensor.kicad_pcb)** | PCB Layout | 2-layer, $100.00 \times 80.00\text{ mm}$ printed circuit board layout. |
| **[`fall_sensor.kicad_pro`](fall_sensor.kicad_pro)** | Project Config | KiCad project workspace and design rules. |
| **[`FallSensor.kicad_sym`](FallSensor.kicad_sym)** | Symbol Library | Custom schematic symbols for breakout modules. |
| **[`FallSensor.pretty/`](FallSensor.pretty/)** | Footprint Library | Custom PCB footprints for daughterboards and sensors. |
| **[`export/`](export/)** | Production Files | Manufacturing Gerbers and printable PDF packages. |

---

## 📐 PCB Specifications

* **Board Dimensions:** $100.00\text{ mm} \times 80.00\text{ mm}$
* **Layer Count:** 2-Layer FR4 ($1.6\text{ mm}$ thickness, $1\text{ oz}$ / $35\mu\text{m}$ copper)
* **Design Rule Status:** **0 DRC Errors, 0 Unconnected Nets**
* **Power Architecture:** Dual switched rails (Protected Li-Ion Battery $\rightarrow$ 5.0V Boost $\rightarrow$ 3.3V Step-Down).
* **Radar Gating:** High-side/low-side N-Channel MOSFET load switch controlled via GPIO 27.

---

## 📌 Microcontroller Pinout & Net Mapping

### ESP32 DevKit V1 (30-Pin) Net Connections
| Pin # | Label | Connected Net | Hardware Destination & Role |
|:---:|---|---|---|
| **1** | `3V3` | `+3V3` | Regulated 3.3V power input from U7 buck converter |
| **5** | `GPIO34` | `/BATT_ADC` | Midpoint of 100kΩ/100kΩ battery sensing divider |
| **8** | `GPIO33` | `Net-(U1-GPIO33)` | Tactile Sync & Alarm Clear Button (`SW1`) |
| **9** | `GPIO25` | `/PRESENCE` | C1001 radar hardware presence flag (`OUT1`) |
| **10** | `GPIO26` | `/FALL` | C1001 radar hardware fall detection flag (`OUT2`) |
| **11** | `GPIO27` | `/RADAR_EN` | Load switch gate control (energizes radar power rail) |
| **14** | `GND` | `GND` | Common system ground plane |
| **15** | `GPIO13` | `/PIR_WAKE` | Motion wake interrupt from ATtiny85 Sentinel (`PB2`) |
| **19** | `GPIO19` | `Net-(U1-GPIO19)` | Status Fall Alarm LED (`D1`) via 270Ω resistor |
| **26** | `GPIO17` | `/RADAR_RX` | Hardware UART RX $\leftarrow$ C1001 radar TX |
| **27** | `GPIO16` | `/RADAR_TX` | Hardware UART TX $\rightarrow$ C1001 radar RX |
| **28** | `GPIO4` | `/MIC_WAKE` | Acoustic impact wake interrupt from ATtiny85 Sentinel (`PB0`) |

### ATtiny85 Sentinel Pin Mapping
| Pin # | Label | Connected Net | Hardware Destination & Role |
|:---:|---|---|---|
| **2** | `PB4` | `Net-(U2-P4)` | Digital acoustic trigger input from LM393 (`DO`) |
| **5** | `PB1` | `Net-(PIR1-OUT)` | Digital motion trigger input from AM312 PIR (`OUT`) |
| **6** | `PB0` | `/MIC_WAKE` | Active-HIGH 50ms wake pulse to ESP32 `GPIO4` |
| **4** | `PB2` | `/PIR_WAKE` | Active-HIGH 50ms wake pulse to ESP32 `GPIO13` |
| **7** | `GND` | `GND` | Common ground |
| **8** | `VIN` | `+5V` | Regulated 5.0V power rail |

---

## 📦 Manufacturing & Test Deliverables

* **Gerber Package:** [`export/fall_sensor_gerbers.zip`](export/fall_sensor_gerbers.zip) — Ready for direct upload to JLCPCB, PCBWay, or OSH Park.
* **1:1 True Scale Paper Testing Sheet:** [`export/pdf/fall_sensor_pcb_front_and_back_A4.pdf`](export/pdf/fall_sensor_pcb_front_and_back_A4.pdf) — Verified 1:1 A4 sheet with 10.0 cm calibration ruler for physical component fit-testing.
* **Assembly & Layer Drawings:** See [`export/pdf/README.md`](export/pdf/README.md) for top/bottom silkscreen and layer plots.

---

## 📖 Detailed Engineering References
* Complete 21-component netlist and verification tables: [`../docs/PCB_Component_Connections_Verification.md`](../docs/PCB_Component_Connections_Verification.md)
* Physical package outlines, drill sizes, and pad-to-pad pitches: [`../docs/PCB_Component_Footprints_and_Dimensions.md`](../docs/PCB_Component_Footprints_and_Dimensions.md)
* Production SMD Component Master List (Rev B): [`../docs/SMD_BOM_Master_List.md`](../docs/SMD_BOM_Master_List.md)
