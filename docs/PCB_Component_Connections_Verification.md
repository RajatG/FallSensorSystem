# 🔌 Fall Sensor System — Master Component Pinout & Net Connection List

> **PCB Revision:** Rev A (Prototype) | **Total Components:** 21 | **DRC Status:** 0 Errors, 0 Unconnected Nets

Use this document to manually verify each connection on the physical PCB or schematic.

---

## 1. 🔋 Power Management Subsystem

### `BT1` — Battery Input Connector (1S Li-Ion 3.7V)
| Pin # | Pin Name | Connected Net | Destination / Purpose |
|---|---|---|---|
| **Pin 1** | BAT- | `Net-(BT1-Pin_1)` | Connects to TP4056 `BAT-` (Pin 2) |
| **Pin 2** | BAT+ | `Net-(BT1-Pin_2)` | Connects to TP4056 `BAT+` (Pin 1) |

---

### `U4` — TP4056 Li-Ion Charger Module
| Pin # | Pin Name | Connected Net | Destination / Purpose |
|---|---|---|---|
| **Pin 1** | BAT+ | `Net-(BT1-Pin_2)` | Li-Ion Battery Positive terminal |
| **Pin 2** | BAT- | `Net-(BT1-Pin_1)` | Li-Ion Battery Negative terminal |
| **Pin 3** | OUT+ | `Net-(U4-OUT+)` | Protected raw battery output $\rightarrow$ SW2 (Pin 1), R1 (Pin 1), C1 (Pin 1) |
| **Pin 4** | OUT- | `GND` | Common Ground Plane |

---

### `SW2` — Main Latching Power Switch
| Pin # | Pin Name | Connected Net | Destination / Purpose |
|---|---|---|---|
| **Pin 1** | Input | `Net-(U4-OUT+)` | Raw battery voltage from TP4056 `OUT+` |
| **Pin 2** | Output | `Net-(U3-VIN+)` | Switched battery power to MT3608 Boost `VIN+` |

---

### `U3` — MT3608 Boost Converter (3.7V $\rightarrow$ 5.0V Rail)
| Pin # | Pin Name | Connected Net | Destination / Purpose |
|---|---|---|---|
| **Pin 1** | VIN+ | `Net-(U3-VIN+)` | Switched battery input from SW2 (Pin 2) |
| **Pin 2** | VIN- | `GND` | Common Ground Plane |
| **Pin 3** | VOUT+ | `+5V` | Regulated **+5V Main System Power Rail** (feeds C3, C4, U6 Pin 1, U7 Pin 1) |
| **Pin 4** | GND | `GND` | Common Ground Plane |

---

### `U7` — Buck Converter Step-Down (5.0V $\rightarrow$ 3.3V Rail)
| Pin # | Pin Name | Connected Net | Destination / Purpose |
|---|---|---|---|
| **Pin 1** | IN+ | `+5V` | +5V Rail from MT3608 Boost |
| **Pin 2** | GND | `GND` | Common Ground Plane |
| **Pin 3** | OUT+ | `+3V3` | Regulated **+3.3V Main System Power Rail** (feeds ESP32, ATtiny85, LM393, PIR1, SW1, C7, C8) |
| **Pin 4** | GND | `GND` | Common Ground Plane |

---

## 2. 🧠 Microcontrollers & Co-Processors

### `U1` — ESP32 DevKit V1 (Main Microcontroller)
| Pin # | Pin Label | Connected Net | Destination / Function |
|---|---|---|---|
| **Pin 1** | `3V3` | `+3V3` | Primary +3.3V power input from U7 |
| **Pin 2** | `EN` | *Unconnected* | Handled internally by DevKit onboard reset |
| **Pin 3** | `GPIO36 (VP)` | *Unconnected* | Floating |
| **Pin 4** | `GPIO39 (VN)` | *Unconnected* | Floating |
| **Pin 5** | `GPIO34` | `/BATT_ADC` | Battery Voltage Divider midpoint (R1/R2) |
| **Pin 6** | `GPIO35` | *Unconnected* | Floating |
| **Pin 7** | `GPIO32` | *Unconnected* | Floating |
| **Pin 8** | `GPIO33` | `Net-(U1-GPIO33)` | Tactile Sync / Disarm Push Button (SW1) |
| **Pin 9** | `GPIO25` | `/PRESENCE` | Radar Hardware Presence flag from RADAR1 (Pin 5) |
| **Pin 10** | `GPIO26` | `/FALL` | Radar Hardware Fall Detection flag from RADAR1 (Pin 6) |
| **Pin 11** | `GPIO27` | `/RADAR_EN` | Load Switch Gate Control $\rightarrow$ U6 DBVT Enable (Pin 3) |
| **Pin 12** | `GPIO14` | *Unconnected* | Floating |
| **Pin 13** | `GPIO12` | *Unconnected* | Floating |
| **Pin 14** | `GND` | `GND` | Common Ground Plane |
| **Pin 15** | `GPIO13` | `/PIR_WAKE` | Motion Wake Interrupt from ATtiny85 (P2 / Pin 4) |
| **Pin 16** | `VIN` | *Unconnected* | DevKit 5V input (bypassed via Pin 1 3V3) |
| **Pin 17** | `GND` | `GND` | Common Ground Plane |
| **Pin 18** | `GPIO23` | *Unconnected* | Floating |
| **Pin 19** | `GPIO22` | *Unconnected* | Floating |
| **Pin 20** | `TX0` | *Unconnected* | DevKit USB-UART bridge |
| **Pin 21** | `RX0` | *Unconnected* | DevKit USB-UART bridge |
| **Pin 22** | `GPIO21` | *Unconnected* | Floating |
| **Pin 23** | `GPIO19` | `Net-(U1-GPIO19)` | Fall Alarm Visual Siren LED driver $\rightarrow$ R3 (Pin 1) |
| **Pin 24** | `GPIO18` | *Unconnected* | Floating |
| **Pin 25** | `GPIO5` | *Unconnected* | Floating |
| **Pin 26** | `GPIO17` | `/RADAR_RX` | ESP32 UART RX $\leftarrow$ RADAR1 TX (Pin 3) |
| **Pin 27** | `GPIO16` | `/RADAR_TX` | ESP32 UART TX $\rightarrow$ RADAR1 RX (Pin 4) |
| **Pin 28** | `GPIO4` | `/MIC_WAKE` | Acoustic Thud Wake Interrupt from ATtiny85 (P0 / Pin 6) |
| **Pin 29** | `GPIO2` | *Unconnected* | Floating (DevKit onboard blue LED) |
| **Pin 30** | `GPIO15` | *Unconnected* | Floating |

---

### `U2` — Digispark ATtiny85 (Ultra-Low Power Wake Sentinel)
| Pin # | Pin Label | Connected Net | Destination / Function |
|---|---|---|---|
| **Pin 1** | `P5 / RESET` | *Unconnected* | Hardware Reset (internally pulled up) |
| **Pin 2** | `P4 (ADC2)` | `Net-(U2-P4)` | Acoustic Thud Input from LM393 `DO` (Pin 3) |
| **Pin 3** | `P3` | *Unconnected* | Floating |
| **Pin 4** | `P2 (SCK)` | `/PIR_WAKE` | 50ms Motion Wake pulse $\rightarrow$ ESP32 GPIO 13 |
| **Pin 5** | `P1 (MISO)` | `Net-(PIR1-OUT)` | Motion Signal Input from AM312 PIR (Pin 2) |
| **Pin 6** | `P0 (AREF)` | `/MIC_WAKE` | 50ms Acoustic Thud Wake pulse $\rightarrow$ ESP32 GPIO 4 |
| **Pin 7** | `GND` | `GND` | Common Ground Plane |
| **Pin 8** | `VIN` | *Unconnected* | Onboard regulator 5V input (bypassed) |
| **Pin 9** | `5V / VCC` | `+3V3` | Power Input ($< 1\text{ µA}$ deep sleep at 3.3V) |

---

## 3. 📡 Radar Detection Subsystem

### `U6` — DBVT SOT-23-6 Load Switch (Radar Power Gating)
| Pin # | Pin Name | Connected Net | Destination / Purpose |
|---|---|---|---|
| **Pin 1** | VIN | `+5V` | Always-on +5V rail from MT3608 Boost |
| **Pin 2** | GND | `GND` | Common Ground Plane |
| **Pin 3** | EN | `/RADAR_EN` | Active-High radar power gate from ESP32 GPIO 27 |
| **Pin 4** | GND | `GND` | Common Ground Plane |
| **Pin 5** | GND | `GND` | Common Ground Plane |
| **Pin 6** | VOUT | `Net-(RADAR1-VIN)` | Switched +5V power feed $\rightarrow$ RADAR1 VIN (Pin 1) |

---

### `RADAR1` — C1001 60GHz Millimeter-Wave Fall Detection Radar
| Pin # | Pin Name | Connected Net | Destination / Purpose |
|---|---|---|---|
| **Pin 1** | VIN | `Net-(RADAR1-VIN)` | Gated +5V power from U6 Load Switch (Pin 6) |
| **Pin 2** | GND | `GND` | Common Ground Plane |
| **Pin 3** | TX | `/RADAR_TX` | Radar Serial Data Out $\rightarrow$ ESP32 GPIO 16 (RX) |
| **Pin 4** | RX | `/RADAR_RX` | Radar Serial Data In $\leftarrow$ ESP32 GPIO 17 (TX) |
| **Pin 5** | OUT1 | `/PRESENCE` | GPIO Fast-Path Presence Flag $\rightarrow$ ESP32 GPIO 25 |
| **Pin 6** | OUT2 | `/FALL` | GPIO Fast-Path Dynamic Fall Flag $\rightarrow$ ESP32 GPIO 26 |

---

## 4. 👁️ Sentinel Sensors (PIR Motion & Acoustic Thud)

### `PIR1` — AM312 Low-Power PIR Motion Sensor
| Pin # | Pin Name | Connected Net | Destination / Purpose |
|---|---|---|---|
| **Pin 1** | VCC | `+3V3` | +3.3V Power Rail |
| **Pin 2** | OUT | `Net-(PIR1-OUT)` | Motion output signal $\rightarrow$ ATtiny85 Pin 5 (P1) |
| **Pin 3** | GND | `GND` | Common Ground Plane |

> [!NOTE]
> **Orientation:** Body is flipped horizontally towards the **RIGHT** ($X \in [124.0, 144.0]$) into the wide-open copper zone, completely clear of C4 and C8.

---

### `U5` — LM393 Sound / Acoustic Thud Sensor Module
| Pin # | Pin Name | Connected Net | Destination / Purpose |
|---|---|---|---|
| **Pin 1** | VCC | `+3V3` | +3.3V Power Rail |
| **Pin 2** | GND | `GND` | Common Ground Plane |
| **Pin 3** | DO | `Net-(U2-P4)` | Digital Thud Output $\rightarrow$ ATtiny85 Pin 2 (P4) |
| **Pin 4** | AO | *Unconnected* | Analog audio output (not used in digital wake design) |

---

## 5. 🎛️ User Interface & Peripherals

### `SW1` — Tactile Sync / Fall Disarm Push Button (4-Pin)
| Pin # | Connected Net | Destination / Purpose |
|---|---|---|
| **Pins 1 & 1** | `Net-(U1-GPIO33)` | Button switch contact $\rightarrow$ ESP32 GPIO 33 |
| **Pins 2 & 2** | `+3V3` | Pulled high to +3.3V on button press |

---

### `D1` — Fall Alarm Visual Siren LED (3mm Red)
| Pin # | Pin Name | Connected Net | Destination / Purpose |
|---|---|---|---|
| **Pin 1** | Anode (A) | `Net-(D1-A)` | Driven by R3 current limiting resistor |
| **Pin 2** | Cathode (K) | `GND` | Common Ground Plane |

---

## 6. ⚡ Resistors & Capacitors (THT 5-Capacitor Architecture)

| Component | Value | Package | Pin 1 Net | Pin 2 Net | Circuit Role |
|---|---|---|---|---|---|
| **`R1`** | 100kΩ | Axial 10.16mm | `Net-(U4-OUT+)` | `/BATT_ADC` | Battery Voltage Divider (Upper arm) |
| **`R2`** | 100kΩ | Axial 10.16mm | `/BATT_ADC` | `GND` | Battery Voltage Divider (Lower arm $\rightarrow$ 50% ratio) |
| **`R3`** | 270Ω | Axial 10.16mm | `Net-(U1-GPIO19)` | `Net-(D1-A)` | Current Limiting Resistor for Alarm LED D1 |
| **`C1`** | 10µF | Disc THT 5.0mm | `Net-(U4-OUT+)` | `GND` | Boost Input Stabilization (smooths battery voltage into MT3608) |
| **`C3`** | 470µF | Radial THT 5.0mm | `+5V` | `GND` | Main Water Tower Bulk Capacitor (absorbs Wi-Fi current spikes) |
| **`C4`** | 22µF | Radial THT 5.0mm | `+5V` | `GND` | Boost Output Filter (smooths 1.2MHz switching ripple) |
| **`C7`** | 0.1µF | Disc THT 5.0mm | `+3V3` | `GND` | ATtiny85 High-Frequency Decoupling |
| **`C8`** | 0.1µF | Disc THT 5.0mm | `+3V3` | `GND` | LM393 Sound Sensor High-Frequency Decoupling |
