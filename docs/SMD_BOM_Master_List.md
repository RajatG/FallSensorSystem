# Production SMD PCB - Master Component Selection & BOM List

This master document specifies all surface-mount device (SMD) integrated circuits, protection components, connectors, and passives required to convert the prototype into a commercial, high-reliability PCB for the Fall Sensor system.

---

## 1. Core Microcontrollers & Processing

| Ref Designator | Function | Recommended SMD Part Number | Package | Description / Justification |
|----------------|----------|----------------------------|---------|-----------------------------|
| **U1** | Main Microcontroller (Wi-Fi/BLE) | **ESP32-WROOM-32E-N4** | SMD Module (18×25.5mm) | FCC/CE pre-certified module with integrated 3D PCB antenna, 4MB Flash. Avoids raw chip RF tuning complexity. |
| **U2** | Sentinel Co-Processor | **ATtiny85-20SU** | SOIC-8 (150mil) | Ultra-low power co-processor (<0.2µA sleep). Manages PIR & MIC interrupts to keep ESP32 asleep. |

---

## 2. Power Management & Charger ICs

| Ref Designator | Function | Recommended SMD Part Number | Package | Description / Justification |
|----------------|----------|----------------------------|---------|-----------------------------|
| **U4A** (Option 1) | Li-Ion Charger w/ Power-Path | **Texas Instruments BQ24075RGTR** | VQFN-16 (3×3mm) | **Gold Standard:** 1.5A charger with Dynamic Power-Path. Runs system off USB power while independently charging battery. |
| **U4B** (Option 2) | Standalone Li-Ion Charger | **Texas Instruments BQ24040DSQR** / **BQ24050** | WSON-10 (2×2mm) | 800mA Linear Charger IC with 30V input tolerance, auto-charge termination, and NTC thermistor pin. |
| **U4C** (Option 3) | Integrated Power Bank PMIC | **Injoinic IP5306** | SOP-8 | **All-in-One Budget Option:** Combines 2.1A Charger + 5V 2.4A Synchronous Boost + 4-LED Fuel Gauge in 1 IC. |
| **U3** | 3.7V to 5V Step-Up Boost | **MT3608** / **SX1308** | SOT-23-6 | High-frequency 1.2MHz boost converter to generate 5V rail for Radar sensor. |
| **U6** | 3.3V LDO Regulator | **TLV75533PDBVR** (or **AMS1117-3.3**) | SOT-23-5 | Ultra-low quiescent current (31µA) 500mA 3.3V LDO regulator for ESP32 and logic. |

---

## 3. Battery Protection Circuit Module (PCM) & Safety

| Ref Designator | Function | Recommended SMD Part Number | Package | Description / Justification |
|----------------|----------|----------------------------|---------|-----------------------------|
| **U8** | Over-Charge / Under-Voltage IC | **DW01A** (or **DW01-P**) | SOT-23-6 | Precision battery protection controller. Cuts discharge at 2.8V (UVLO) and charge at 4.25V. |
| **Q2** | Dual N-Channel Power MOSFET | **FS8205A** | TSSOP-8 | High-density 20V 6A dual N-MOSFET driven by DW01A for high-side/low-side disconnect. |
| **Q3** | Reverse Polarity Protection | **AO3401A** (or **Si2301CDS**) | SOT-23 | P-Channel MOSFET on battery positive rail to prevent catastrophic damage if battery leads are reversed. |
| **D2** | USB-C ESD Protection Array | **USBLC6-2SC6** | SOT-23-6 | Low-capacitance ESD protection diode array for VBUS, D+, D- lines (15kV ESD protection). |
| **NTC1** | Battery Thermal Sensor | **10K NTC Thermistor** (0805) | 0805 | Placed adjacent to battery holder, wired to Charger TS pin to halt charging outside 0°C–45°C. |

---

## 4. Sensors & Acoustic Detection Circuitry

| Ref Designator | Function | Recommended SMD Part Number | Package | Description / Justification |
|----------------|----------|----------------------------|---------|-----------------------------|
| **RADAR1** | Radar Interface Header | **2.54mm Pitch 1x6 Header** (or Direct Solder Pads) | SMT / TH | Interfaces C1001 60GHz or LD2410 24GHz Radar module. |
| **U5** | Acoustic Dual Comparator | **LM393G** / **LM393LV** | SOIC-8 | Dual differential comparator for LM393 sound thud sensor module. |
| **MIC1** | Electret Microphone | **CMA-4544PF-W** (or **SMD Mic**) | 6mm DIP/SMD | Electret microphone capsule for sound impulse pickup. |
| **PIR1** | Passive Infrared Sensor | **AS312** (or **AM312 Element**) | SOT-23-6 / TO-5 | Digital PIR sensor element with integrated delay controller. |
| **Q1** | Radar Power-Gating MOSFET | **AO3400A** (or **BSS138**) | SOT-23 | N-Channel MOSFET controlled by GPIO 27 to cut 5V power to Radar when sleeping. |

---

## 5. Battery Connectors, Switches & User Interface

| Ref Designator | Function | Recommended SMD Part Number | Package | Description / Justification |
|----------------|----------|----------------------------|---------|-----------------------------|
| **J1** | Battery Cable Connector | **JST-PH-2.0mm S2B-PH-K-S** | SMT Right-Angle | **Industry Standard:** 2-pin keyed connector for Li-Ion / LiPo battery packs. |
| **J2** (Alt) | On-Board 21700 Battery Clip | **Keystone 1048** / **1042** | SMT Clips | Mounted directly on back of PCB for wireless 21700/18650 cell insertion. |
| **J3** | USB-C Power / Charging Input | **TYPE-C-31-M-12** (16-Pin) | SMT Mid-Mount | 16-pin USB-C receptacle for 5V power input. Uses 5.1k pull-down resistors on CC1/CC2 lines. |
| **SW2** | Main System Power Switch | **SK-12D07** / **SS-12D00** | SMT 3-Pin | Low-profile SMT slide switch. |
| **SW1** | Sync / Manual Wake Button | **EVQ-P7A01K** (3×4mm) | SMT Tactile | Momentary push button connected to GPIO 33. |
| **D1** | Fall Siren Alarm LED | **0805 Red LED** | 0805 SMT | High-brightness red LED driven by GPIO 19. |
| **D3** | Charge Status LED | **0805 Green/Amber Dual LED** | 0805 SMT | Driven by STAT1/STAT2 pins of BQ24075 / TP4056. |

---

## 6. Passives & Value Specification

| Component | Value / Rating | Package | Purpose |
|-----------|----------------|---------|---------|
| **R1, R2** | **1MΩ (1%)** | 0805 | Battery Voltage Divider (connected to GPIO 34). 1MΩ values reduce battery drain to <1.8µA! |
| **R3** | **270Ω** | 0805 | Current-limiting resistor for Fall Alarm LED. |
| **R4** | **10kΩ** | 0805 | Pull-down resistor on MOSFET Gate (GPIO 27). |
| **R5, R6** | **5.1kΩ (1%)** | 0603 | CC1 & CC2 pull-down resistors on USB-C receptacle (required for USB-C PD power delivery). |
| **C1, C2** | **10µF 16V Ceramic** | 0805 | Decoupling capacitors for LDO 3.3V and 5V boost rails. |
| **C3, C4** | **100nF 16V Ceramic** | 0603 | High-frequency bypass capacitors for ESP32 and ATtiny85 VCC pins. |
