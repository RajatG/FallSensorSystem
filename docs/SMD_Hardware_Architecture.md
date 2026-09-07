# Commercial SMD Hardware Architecture & Power Management Design

This guide outlines the transition from a prototype with breakout modules to a compact, production-ready **Surface Mount Device (SMD)** PCB design for the Fall Sensor system.

---

## 1. Complete SMD Component Migration List

Replacing breakout boards with discrete SMD ICs reduces board footprint by **up to 70%** while significantly increasing reliability and lowering unit BOM cost.

| Prototype Breakout Board | Component Function | Recommended Discrete SMD IC / Part | Package Type | Key Advantages |
|--------------------------|--------------------|-----------------------------------|--------------|----------------|
| **ESP32 DevKit V1** | Main Microcontroller | **ESP32-WROOM-32E** (or ESP32-WROOM-32UE with U.FL antenna) | SMD Module (18x25.5mm) | Integrated RF shielding, FCC/CE certified, compact footprint. |
| **Digispark ATtiny85** | Sentinel Co-Processor | **ATtiny85-20SU** (or ATtiny45-10SU) | SOIC-8 (150mil) | Tiny 5x4mm IC, ultra-low power deep sleep (<1µA). |
| **TP4056 Charger Board** | 1S Li-Ion Charger | **TP4056** (or **TP4057** / **LTC4054**) | SOT-23-6 / SOP-8-PP | 1A linear charger IC with LED status pins. |
| **MT3608 Boost Board** | 3.7V to 5V Step-Up | **MT3608** (or **TPS61099** / **SX1308**) | SOT-23-6 | 1.2MHz high-efficiency boost IC. |
| **LM393 Sound Module** | Acoustic Thud Sensor | **LM393G** / **LM393LV** Dual Comparator + Electret Mic Capsule | SOIC-8 / 6mm Mic | Discrete SMD comparator + SMT electret mic. |
| **AM312 PIR Module** | Motion Detection | **AS312** (or **PIR sensor element + BISS0001 IC**) | SOT-23-6 / TO-5 | Compact surface-mount PIR sensor element. |
| **Load Switch Socket (U6)** | Radar Power Switch | **TPS22918DBVT** (or **BSS138** / **AO3400A**) | SOT-23-6 | High-efficiency load switch IC with integrated slew rate control. |
| **LM2596 Buck Module (U7)** | 5V to 3.3V Step-Down | **TLV75533PDBVR** (or **AMS1117-3.3**) | SOT-23-5 | Ultra-low Iq 3.3V LDO regulator replacing bulky prototype buck module. |
| **Power Switch SW2** | System Power Switch | **SS-12D00** / **SK-12D07** SMT Slide Switch | SMT 3-Pin | Low-profile surface-mount slide switch. |
| **Sync Button SW1** | Reset / BLE Button | **EVQ-P7A01K** 3x4mm SMT Tactile Switch | SMT 2-Pin | Soft-touch SMT push button. |
| **Passives (R1-R3, D1, 5 Caps)** | Resistors, LED, Caps | 0805 or 0603 SMD Resistors / 0805 LED / MLCC | 0805 / 0603 SMT | Standard SMT surface mount passives (C1, C3, C4, C7, C8). |

---

## 2. Essential Battery Protection & Professional Circuitry

A commercial battery-powered IoT device requires robust hardware protection to meet CE/FCC/UL safety standards:

```
[ USB-C Plug ] ---> [ USBLC6-2SC6 (ESD Protection) ]
                         |
                         v
[ P-MOSFET Reverse Polarity ] ---> [ TP4056 Charger IC ]
                                         |
                                         v
                     [ DW01A + FS8205A (Over-Charge / Over-Discharge PCM) ]
                                         |
                                         v
                              [ 3.7V Li-Ion Battery ]
```

### Essential Protection Components:
1. **Under-Voltage Lockout (UVLO / Over-Discharge Protection):**
   * **IC Combo:** **DW01A** (Protection Controller IC) + **FS8205A** (Dual N-Channel MOSFET in TSSOP-8).
   * **Function:** Automatically disconnects the battery if voltage drops below **2.8V** to prevent permanent cell damage or chemical swelling.
2. **Over-Charge Protection:**
   * Cuts off charging automatically at **4.25V ± 0.05V**.
3. **Over-Current & Short-Circuit Protection:**
   * DW01A detects short circuits and shuts off the dual MOSFET within microseconds if current exceeds ~3A.
4. **Reverse Polarity Protection:**
   * A **P-Channel MOSFET (e.g. AO3401A)** placed on the battery positive line prevents catastrophic component destruction if the battery leads are accidentally reversed during assembly.
5. **USB-C Input ESD Protection:**
   * **USBLC6-2SC6** (SOT-23-6) placed on VBUS and D+/D- lines protects sensitive electronics against 15kV static discharge when plugging in the USB cable.
6. **Thermal / NTC Thermistor Protection:**
   * Connecting a 10K NTC thermistor attached to the battery pack to the TEMP pin of the charger IC prevents charging if battery temperature is < 0°C or > 45°C.

---

## 3. Power Architecture Optimization: Breakout Modules vs. Integrated Power-Path Solutions

### Evaluating Combined Modules (J5019 / IP5306 / BQ24075)

While module boards like the **J5019** (combined TP4056 + MT3608) save wiring space, they suffer from a major design flaw known as **Lack of Power-Path Management**.

#### The "No Power-Path" Problem:
If you charge a battery while the ESP32 is drawing current from the same rail:
- The TP4056 charger cannot distinguish between battery charge current and system operating current.
- The charger fails to detect the 1/10th termination current threshold, causing the battery to **overcharge, overheat, or loop-charge continuously**.

```
❌ BAD (No Power-Path):
USB 5V ---> Charger ---> [ Battery + ESP32 Load (Shared Rail) ]  (Continuous loop charging)

✅ GOOD (Hardware Power-Path):
USB 5V ---> [ Power-Path Switch ] ---> ESP32 System Rail (Direct 5V)
                     |
                     +-------------> Charger ---> Battery (Isolated charging)
```

### Recommended Integrated Power Management ICs (PMICs):

1. **Texas Instruments BQ24075 (Professional Gold Standard):**
   * **Features:** Integrated 1.5A 1S Li-Ion Charger + **Dynamic Power-Path Management**.
   * **Advantage:** When USB is plugged in, it powers the ESP32 directly from USB while independently charging the battery. When USB is unplugged, it seamlessly switches system power to the battery with 0ms delay.
2. **Injoinic IP5306 (Compact Power Bank SoC):**
   * **Features:** Fully integrated 2.1A Charger + 5V 2.4A Synchronous Boost Converter in an SOP-8 package.
   * **Advantage:** Single chip replaces TP4056 + MT3608 + DW01A. Very low cost and extremely compact.
3. **MPS MP2617:**
   * **Features:** 3A Single-Cell NVDC Buck Charger with Power-Path.

---

## 4. Multi-Battery Cell Setup Considerations (2P vs 2S)

If expanding to a multi-battery setup for extended operating life:

### Option A: 2P Setup (2 Cells in Parallel - 3.7V Nominal, Double Ah Capacity)
* **Voltage:** 3.7V Nominal (4.2V Max).
* **System Compatibilty:** Compatible with 1S Charger ICs (TP4056 / BQ24075).

> [!CAUTION]
> **2P Critical Precautions:**
> 1. **Cell Voltage Matching:** Both battery cells **MUST be matched to within 0.05V** before connecting in parallel. If a 4.2V cell is connected in parallel with a 3.0V cell, a violent cross-charging current (>10A) will flow instantly, causing thermal runaway or fire!
> 2. **Shared PCM Protection Board:** Use a single 2S/2P rated protection circuit board attached to the combined parallel pack.

---

### Option B: 2S Setup (2 Cells in Series - 7.4V Nominal, 8.4V Max)
* **Voltage:** 7.4V Nominal (8.4V Max).
* **System Compatibility:** Requires an **8.4V Step-Down (Buck) Regulator** (e.g. MP2307 / TPS62130) to generate system 5V / 3.3V efficiently without heat.

> [!WARNING]
> **2S Critical Precautions:**
> 1. **Cell Balancing Required:** A **2S BMS with Active or Passive Cell Balancing** (e.g. **HY2120** or **S-8254A**) is **MANDATORY**. Over time, one cell will charge faster than the other; without cell balancing, one cell will overcharge to >4.35V while the other remains undercharged.
> 2. **Charger IC:** Standard TP4056 (4.2V) CANNOT be used. You must use a dedicated 2S series charger IC like the **TP5100** (supports 1S/2S) or **BQ24725A**.
