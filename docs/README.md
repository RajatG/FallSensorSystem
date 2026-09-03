# 📚 Fall Sensor System — Master Documentation Hub

Welcome to the technical engineering documentation for the Fall Sensor System. This directory contains the complete architectural specifications, firmware state machines, hardware verification guides, and production roadmaps.

---

## 🧭 Complete Documentation Flow

```
                                  [ Root README ]
                                         │
                 ┌───────────────────────┴───────────────────────┐
                 │                                               │
    [ 1. System Roadmap & Specs ]                  [ 2. Firmware Architecture ]
    Master_4Stream_Roadmap_and_                   Firmware_Architecture_and_
    Recommendations.md                            Detection_Logic.md
                 │                                               │
        ┌────────┴────────┐                             ┌────────┴────────┐
        │                 │                             │                 │
  [ SMD Architecture ] [ SMD BOM ]             [ Radar Early Exit ]  [ MIC Sentinel ]
  SMD_Hardware_        SMD_BOM_                C1001_Early_Exit_     ATtiny85_MIC_
  Architecture.md      Master_List.md          Analysis.md           Analysis.md
                 │
    [ 3. PCB Hardware Verification ]
    ├── PCB_Component_Connections_Verification.md
    └── PCB_Component_Footprints_and_Dimensions.md
```

---

## 📑 Document Catalog

### 1. 📋 System Roadmaps & Product Architecture
* **[`Master_4Stream_Roadmap_and_Recommendations.md`](Master_4Stream_Roadmap_and_Recommendations.md)**  
  *Executive summary of all 4 engineering streams (Firmware, PCB Hardware, 3D Enclosure, Android App), including current completion percentages, milestones, and the complete Rev B SMD production transition plan.*
* **[`SMD_Hardware_Architecture.md`](SMD_Hardware_Architecture.md)**  
  *Production hardware architecture: discrete TP4056 charging, MT3608 boost, DW01A battery protection, USBLC6-2SC6 ESD suppression, power-path PMIC, and thermal cutoff specs.*
* **[`SMD_BOM_Master_List.md`](SMD_BOM_Master_List.md)**  
  *Complete Bill of Materials for automated SMT pick-and-place assembly (LCSC / JLCPCB part numbers).*

---

### 2. 🧠 Firmware & Sensor Signal Processing
* **[`Firmware_Architecture_and_Detection_Logic.md`](Firmware_Architecture_and_Detection_Logic.md)**  
  *Complete end-to-end firmware guide: Deep sleep power states, wakeup interrupts, radar warmup and early exit sequence, the 4-layer fall detection pipeline (Acoustic $\rightarrow$ Dynamic $\rightarrow$ Floor Level $\rightarrow$ Gradual Posture Collapse), and BLE telemetry protocol.*
* **[`C1001_Early_Exit_Analysis.md`](C1001_Early_Exit_Analysis.md)**  
  *In-depth timing breakdown of C1001 60GHz UART loop latency, double-call bug fixes, and the 2.5s early exit logic that yields up to ~90% power savings.*
* **[`ATtiny85_MIC_Analysis.md`](ATtiny85_MIC_Analysis.md)**  
  *Acoustic impact sensitivity analysis: ATtiny85 $V_{IH}$ logic threshold matching, LM393 open-collector pull-up configurations, and hardware interrupt debounce.*

---

### 3. 🔌 Hardware Verification & PCB Guides
* **[`PCB_Component_Connections_Verification.md`](PCB_Component_Connections_Verification.md)**  
  *Master netlist and pinout verification guide for all 21 components on the Rev A PCB.*
* **[`PCB_Component_Footprints_and_Dimensions.md`](PCB_Component_Footprints_and_Dimensions.md)**  
  *Complete physical package dimensions, drill hole diameters, and pad-to-pad pitches for physical prototyping.*

---

## 🖨️ Fabrication & Printable Deliverables

* **PCB 1:1 Scale Paper Test Sheet:** [`../hardware/export/pdf/fall_sensor_pcb_front_and_back_A4.pdf`](../hardware/export/pdf/fall_sensor_pcb_front_and_back_A4.pdf)
* **Production Gerber Package:** [`../hardware/export/fall_sensor_gerbers.zip`](../hardware/export/fall_sensor_gerbers.zip)
* **3D Printed Enclosure STLs & CAD:** [`../enclosure/`](../enclosure/)
