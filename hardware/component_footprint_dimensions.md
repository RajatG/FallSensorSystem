# Fall Sensor PCB - Complete Component Footprint & Dimension Master List

**Board Outline**: `100.00 mm (W) x 80.00 mm (H)` | **Layers**: 2-Layer FR4 (1.6mm)

| Ref | Component / Value | Footprint Package | Physical Outline (W x H) | Pad-to-Pad Pitch / Spacing | Mounting Type / Drill | Board Location (X, Y) |
|---|---|---|---|---|---|---|
| **BT1** | BATTERY_PADS | `PinHeader_1x02_P2.54mm_Vertical` | `3.54 × 6.09 mm` | 2.54 mm (Span: 0.0×2.5mm) | thru_hole (1.00 mm) | (52.5, 128.0) |
| **C1** | 10u | `C_Disc_D5.0mm_W2.5mm_P5.00mm` | `7.10 × 3.00 mm` | 5.00 mm (Span: 5.0×0.0mm) | thru_hole (0.80 mm) | (83.5, 88.0) |
| **C3** | 470u | `CP_Radial_D8.0mm_P3.50mm` | `8.49 × 8.16 mm` | 3.50 mm (Span: 3.5×0.0mm) | thru_hole (0.80 mm) | (89.0, 72.0) |
| **C4** | 22u | `C_Disc_D5.0mm_W2.5mm_P5.00mm` | `7.10 × 3.00 mm` | 5.00 mm (Span: 5.0×0.0mm) | thru_hole (0.80 mm) | (113.5, 52.0) |
| **C7** | 0.1u | `C_Disc_D5.0mm_W2.5mm_P5.00mm` | `7.10 × 3.00 mm` | 5.00 mm (Span: 5.0×0.0mm) | thru_hole (0.80 mm) | (110.0, 76.5) |
| **C8** | 0.1u | `C_Disc_D5.0mm_W2.5mm_P5.00mm` | `7.10 × 3.00 mm` | 5.00 mm (Span: 5.0×0.0mm) | thru_hole (0.80 mm) | (120.0, 54.5) |
| **D1** | LED | `LED_D3.0mm` | `4.84 × 4.42 mm` | 2.54 mm (Span: 2.5×0.0mm) | thru_hole (0.90 mm) | (140.2, 89.0) |
| **PIR1** | AM312_PIR | `AM312_PIR_Square22x20` | `22.00 × 20.00 mm` | 2.54 mm (Span: 5.08×0.0mm) | thru_hole (1.00 mm) | (139.5, 58.25) |
| **R1** | 100k | `R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal` | `12.26 × 3.00 mm` | 10.16 mm (Span: 10.2×0.0mm) | thru_hole (0.80 mm) | (93.0, 121.5) |
| **R2** | 100k | `R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal` | `12.26 × 3.00 mm` | 10.16 mm (Span: 10.2×0.0mm) | thru_hole (0.80 mm) | (92.9, 126.0) |
| **R3** | 270 | `R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal` | `12.26 × 3.00 mm` | 10.16 mm (Span: 10.2×0.0mm) | thru_hole (0.80 mm) | (138.5, 106.7) |
| **RADAR1** | C1001_Radar | `C1001_Module` | `22.00 × 22.00 mm` | 2.54 mm (Span: 0.0×12.7mm) | thru_hole (1.00 mm) | (141.5, 112.0) |
| **SW1** | SYNC | `SW_PUSH_6mm` | `9.50 × 7.50 mm` | 6.50 mm (Span: 6.5×4.5mm) | thru_hole (1.10 mm) | (107.2, 121.2) |
| **SW2** | LATCH_PWR | `PinHeader_1x02_P2.54mm_Vertical` | `3.54 × 6.09 mm` | 2.54 mm (Span: 0.0×2.5mm) | thru_hole (1.00 mm) | (52.5, 114.5) |
| **U1** | ESP32_DevKit_V1 | `ESP32_DevKit_DOIT_2x15` | `39.20 × 29.00 mm` | 2.54 mm (Span: 35.6×25.4mm) | thru_hole (1.00 mm) | (127.5, 109.9) |
| **U2** | Digispark_ATtiny85 | `Digispark_9Pin_RightAngle` | `26.50 × 19.00 mm` | 2.54 mm (L-shape: 12.7 / 5.08mm) | thru_hole (1.016 mm) | (75.9, 119.3) |
| **U3** | MT3608_Module | `MT3608_Module` | `36.00 × 17.00 mm` | 7.62 mm (Span: 29.50×7.62mm) | thru_hole (1.20 mm) | (77.25, 55.70) |
| **U4** | TP4056_Module | `TP4056_Module` | `17.00 × 27.00 mm` | 2x 1x02 (2.54mm pitch, 8.92mm gap, 14.0mm span) | thru_hole (1.00 mm) | (76.0, 103.0) |
| **U5** | LM393_Sound_Module | `LM393_Sound_Module` | `16.62 × 37.00 mm` | 2.54 mm (Span: 7.6×0.0mm) | thru_hole (1.00 mm) | (115.5, 76.8) |
| **U6** | LoadSwitch_DBVT | `SOT-23-6` | `4.10 × 3.40 mm` | 0.95 mm (Span: 2.3×1.9mm) | smd (SMD) | (121.4, 120.5) |
| **U7** | Buck Converter | `LM2596_Module` | `43.18 × 21.08 mm` | 17.15 mm (Span: 17.15×39.50mm) | thru_hole (1.50 mm) | (68.5, 52.5) |


---

## Detailed Pinout & Coordinate Map by Component

### `BT1` - BATTERY_PADS (`Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical`)
- **Physical Dimensions**: `3.54 mm × 6.09 mm`
- **Placement on PCB**: `X = 52.50 mm`, `Y = 128.00 mm`, Rotation = `180.0°` (Layer: F.Cu)
- **Total Pads**: 2 (thru_hole)
| Pad # | Local Offset (X, Y) | Pad Size (W × H) | Pad Shape | Hole Drill |
|---|---|---|---|---|
| **1** | `(0.00, 0.00)` | `1.70 × 1.70 mm` | rect | 1.00 mm |
| **2** | `(0.00, 2.54)` | `1.70 × 1.70 mm` | circle | 1.00 mm |

### `C1` - 10u (`Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm`)
- **Physical Dimensions**: `7.10 mm × 3.00 mm`
- **Placement on PCB**: `X = 83.50 mm`, `Y = 88.00 mm`, Rotation = `-90.0°` (Layer: F.Cu)
- **Total Pads**: 2 (thru_hole)
| Pad # | Local Offset (X, Y) | Pad Size (W × H) | Pad Shape | Hole Drill |
|---|---|---|---|---|
| **1** | `(0.00, 0.00)` | `1.60 × 1.60 mm` | circle | 0.80 mm |
| **2** | `(5.00, 0.00)` | `1.60 × 1.60 mm` | circle | 0.80 mm |

### `C3` - 470u (`Capacitor_THT:CP_Radial_D8.0mm_P3.50mm`)
- **Physical Dimensions**: `8.49 mm × 8.16 mm`
- **Placement on PCB**: `X = 89.00 mm`, `Y = 72.00 mm`, Rotation = `-90.0°` (Layer: F.Cu)
- **Total Pads**: 2 (thru_hole)
| Pad # | Local Offset (X, Y) | Pad Size (W × H) | Pad Shape | Hole Drill |
|---|---|---|---|---|
| **1** | `(0.00, 0.00)` | `1.60 × 1.60 mm` | roundrect | 0.80 mm |
| **2** | `(3.50, 0.00)` | `1.60 × 1.60 mm` | circle | 0.80 mm |

### `C4` - 22u (`Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm`)
- **Physical Dimensions**: `7.10 mm × 3.00 mm`
- **Placement on PCB**: `X = 113.50 mm`, `Y = 52.00 mm`, Rotation = `-90.0°` (Layer: F.Cu)
- **Total Pads**: 2 (thru_hole)
| Pad # | Local Offset (X, Y) | Board Coord (X, Y) | Pad Size (W × H) | Pad Shape | Hole Drill | Net |
|---|---|---|---|---|---|---|
| **1** | `(0.00, 0.00)` | `(113.50, 52.00)` | `1.60 × 1.60 mm` | circle | 0.80 mm | `+5V` |
| **2** | `(5.00, 0.00)` | `(113.50, 57.00)` | `1.60 × 1.60 mm` | circle | 0.80 mm | `GND` |

### `C7` - 0.1u (`Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm`)
- **Physical Dimensions**: `7.10 mm × 3.00 mm`
- **Placement on PCB**: `X = 110.00 mm`, `Y = 76.50 mm`, Rotation = `90.0°` (Layer: F.Cu)
- **Total Pads**: 2 (thru_hole)
| Pad # | Local Offset (X, Y) | Pad Size (W × H) | Pad Shape | Hole Drill |
|---|---|---|---|---|
| **1** | `(0.00, 0.00)` | `1.60 × 1.60 mm` | circle | 0.80 mm |
| **2** | `(5.00, 0.00)` | `1.60 × 1.60 mm` | circle | 0.80 mm |

### `C8` - 0.1u (`Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm`)
- **Physical Dimensions**: `7.10 mm × 3.00 mm`
- **Placement on PCB**: `X = 120.00 mm`, `Y = 54.50 mm`, Rotation = `-90.0°` (Layer: B.Cu)
- **Total Pads**: 2 (thru_hole)
| Pad # | Local Offset (X, Y) | Pad Size (W × H) | Pad Shape | Hole Drill |
|---|---|---|---|---|
| **1** | `(0.00, 0.00)` | `1.60 × 1.60 mm` | circle | 0.80 mm |
| **2** | `(5.00, 0.00)` | `1.60 × 1.60 mm` | circle | 0.80 mm |

### `D1` - LED (`LED_THT:LED_D3.0mm`)
- **Physical Dimensions**: `4.84 mm × 4.42 mm`
- **Placement on PCB**: `X = 142.50 mm`, `Y = 89.00 mm`, Rotation = `0.0°` (Layer: F.Cu) — *Collinear on unified aperture axis $X = 142.50\text{ mm}$*
- **Total Pads**: 2 (thru_hole)
| Pad # | Local Offset (X, Y) | Pad Size (W × H) | Pad Shape | Hole Drill |
|---|---|---|---|---|
| **1** | `(0.00, 0.00)` | `1.80 × 1.80 mm` | rect | 0.90 mm |
| **2** | `(2.54, 0.00)` | `1.80 × 1.80 mm` | circle | 0.90 mm |

### `PIR1` - AM312_PIR (`FallSensor:AM312_PIR_Square22x20`)
- **Physical Dimensions**: `24.00 mm × 20.00 mm` ($\varnothing 12.0\text{ mm}$ dome lens at $13.80\text{ mm}$ offset from header pins)
- **Placement on PCB**: `X = 128.70 mm`, `Y = 56.25 mm`, Rotation = `90.0°` (Layer: F.Cu)
- **Optical Center of Fresnel Dome**: `X = 142.50 mm`, `Y = 53.71 mm` — *Collinear on unified aperture axis $X = 142.50\text{ mm}$*
- **Total Pads**: 3 (thru_hole)
| Pad # | Local Offset (X, Y) | Pad Size (W × H) | Pad Shape | Hole Drill |
|---|---|---|---|---|
| **1** | `(0.00, 0.00)` | `1.80 × 1.80 mm` | rect | 1.00 mm |
| **2** | `(2.54, 0.00)` | `1.70 × 1.70 mm` | circle | 1.00 mm |
| **3** | `(5.08, 0.00)` | `1.80 × 1.80 mm` | circle | 1.00 mm |

### `R1` - 100k (`Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal`)
- **Physical Dimensions**: `12.26 mm × 3.00 mm`
- **Placement on PCB**: `X = 93.00 mm`, `Y = 121.50 mm`, Rotation = `0.0°` (Layer: F.Cu)
- **Total Pads**: 2 (thru_hole)
| Pad # | Local Offset (X, Y) | Pad Size (W × H) | Pad Shape | Hole Drill |
|---|---|---|---|---|
| **1** | `(0.00, 0.00)` | `1.60 × 1.60 mm` | circle | 0.80 mm |
| **2** | `(10.16, 0.00)` | `1.60 × 1.60 mm` | circle | 0.80 mm |

### `R2` - 100k (`Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal`)
- **Physical Dimensions**: `12.26 mm × 3.00 mm`
- **Placement on PCB**: `X = 92.92 mm`, `Y = 126.00 mm`, Rotation = `0.0°` (Layer: F.Cu)
- **Total Pads**: 2 (thru_hole)
| Pad # | Local Offset (X, Y) | Pad Size (W × H) | Pad Shape | Hole Drill |
|---|---|---|---|---|
| **1** | `(0.00, 0.00)` | `1.60 × 1.60 mm` | circle | 0.80 mm |
| **2** | `(10.16, 0.00)` | `1.60 × 1.60 mm` | circle | 0.80 mm |

### `R3` - 270 (`Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal`)
- **Physical Dimensions**: `12.26 mm × 3.00 mm`
- **Placement on PCB**: `X = 138.50 mm`, `Y = 106.66 mm`, Rotation = `90.0°` (Layer: F.Cu)
- **Total Pads**: 2 (thru_hole)
| Pad # | Local Offset (X, Y) | Pad Size (W × H) | Pad Shape | Hole Drill |
|---|---|---|---|---|
| **1** | `(0.00, 0.00)` | `1.60 × 1.60 mm` | circle | 0.80 mm |
| **2** | `(10.16, 0.00)` | `1.60 × 1.60 mm` | circle | 0.80 mm |

### `RADAR1` - C1001_Radar (`FallSensor:C1001_Module`)
- **Physical Dimensions**: `20.50 mm × 20.50 mm`
- **Placement on PCB**: `X = 141.50 mm`, `Y = 112.00 mm`, Rotation = `0.0°` (Layer: F.Cu)
- **Total Pads**: 6 (thru_hole)
| Pad # | Local Offset (X, Y) | Pad Size (W × H) | Pad Shape | Hole Drill |
|---|---|---|---|---|
| **1** | `(0.00, 0.00)` | `1.70 × 1.70 mm` | rect | 1.00 mm |
| **2** | `(0.00, 2.54)` | `1.70 × 1.70 mm` | circle | 1.00 mm |
| **3** | `(0.00, 5.08)` | `1.70 × 1.70 mm` | circle | 1.00 mm |
| **4** | `(0.00, 7.62)` | `1.70 × 1.70 mm` | circle | 1.00 mm |
| **5** | `(0.00, 10.16)` | `1.70 × 1.70 mm` | circle | 1.00 mm |
| **6** | `(0.00, 12.70)` | `1.70 × 1.70 mm` | circle | 1.00 mm |

### `SW1` - SYNC (`Button_Switch_THT:SW_PUSH_6mm`)
- **Physical Dimensions**: `6.00 mm × 6.00 mm` body envelope (Lead span: `6.50 mm × 4.50 mm`)
- **Placement on PCB (Origin / Pin 1)**: `X = 107.25 mm`, `Y = 121.25 mm`, Rotation = `0.0°` (Layer: F.Cu)
- **Actuator Plunger Center (Button Press Center)**: `X = 110.50 mm`, `Y = 123.50 mm`
- **Total Pads**: 4 (thru_hole)
| Pad # | Function / Net | Local Offset (X, Y) | Board Coord (X, Y) | Pad Size (W × H) | Pad Shape | Hole Drill |
|---|---|---|---|---|---|---|
| **1** | `Net-(U1-GPIO33)` | `(0.00, 0.00)` | `(107.25, 121.25)` | `2.00 × 2.00 mm` | circle | 1.10 mm |
| **1** | `Net-(U1-GPIO33)` | `(6.50, 0.00)` | `(113.75, 121.25)` | `2.00 × 2.00 mm` | circle | 1.10 mm |
| **2** | `+3V3` | `(0.00, 4.50)` | `(107.25, 125.75)` | `2.00 × 2.00 mm` | circle | 1.10 mm |
| **2** | `+3V3` | `(6.50, 4.50)` | `(113.75, 125.75)` | `2.00 × 2.00 mm` | circle | 1.10 mm |

### `SW2` - LATCH_PWR (`Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical`)
- **Physical Dimensions**: `3.54 mm × 6.09 mm`
- **Placement on PCB**: `X = 52.50 mm`, `Y = 114.50 mm`, Rotation = `0.0°` (Layer: F.Cu)
- **Total Pads**: 2 (thru_hole)
| Pad # | Local Offset (X, Y) | Pad Size (W × H) | Pad Shape | Hole Drill |
|---|---|---|---|---|
| **1** | `(0.00, 0.00)` | `1.70 × 1.70 mm` | rect | 1.00 mm |
| **2** | `(0.00, 2.54)` | `1.70 × 1.70 mm` | circle | 1.00 mm |

### `U1` - ESP32_DevKit_V1 (`FallSensor:ESP32_DevKit_DOIT_2x15`)
- **Physical Dimensions**: `39.20 mm × 29.00 mm`
- **Placement on PCB**: `X = 127.50 mm`, `Y = 109.86 mm`, Rotation = `180.0°` (Layer: F.Cu)
- **Total Pads**: 30 (thru_hole)
| Pad # | Local Offset (X, Y) | Pad Size (W × H) | Pad Shape | Hole Drill |
|---|---|---|---|---|
| **1** | `(0.00, 0.00)` | `1.70 × 1.70 mm` | rect | 1.00 mm |
| **2** | `(2.54, 0.00)` | `1.70 × 1.70 mm` | circle | 1.00 mm |
| **3** | `(5.08, 0.00)` | `1.70 × 1.70 mm` | circle | 1.00 mm |
| **4** | `(7.62, 0.00)` | `1.70 × 1.70 mm` | circle | 1.00 mm |
| **5** | `(10.16, 0.00)` | `1.70 × 1.70 mm` | circle | 1.00 mm |
| **6** | `(12.70, 0.00)` | `1.70 × 1.70 mm` | circle | 1.00 mm |
| **7** | `(15.24, 0.00)` | `1.70 × 1.70 mm` | circle | 1.00 mm |
| **8** | `(17.78, 0.00)` | `1.70 × 1.70 mm` | circle | 1.00 mm |
| **9** | `(20.32, 0.00)` | `1.70 × 1.70 mm` | circle | 1.00 mm |
| **10** | `(22.86, 0.00)` | `1.70 × 1.70 mm` | circle | 1.00 mm |
| **11** | `(25.40, 0.00)` | `1.70 × 1.70 mm` | circle | 1.00 mm |
| **12** | `(27.94, 0.00)` | `1.70 × 1.70 mm` | circle | 1.00 mm |
| **13** | `(30.48, 0.00)` | `1.70 × 1.70 mm` | circle | 1.00 mm |
| **14** | `(33.02, 0.00)` | `1.70 × 1.70 mm` | circle | 1.00 mm |
| **15** | `(35.56, 0.00)` | `1.70 × 1.70 mm` | circle | 1.00 mm |
| **16** | `(0.00, 25.40)` | `1.70 × 1.70 mm` | circle | 1.00 mm |
| **17** | `(2.54, 25.40)` | `1.70 × 1.70 mm` | circle | 1.00 mm |
| **18** | `(5.08, 25.40)` | `1.70 × 1.70 mm` | circle | 1.00 mm |
| **19** | `(7.62, 25.40)` | `1.70 × 1.70 mm` | circle | 1.00 mm |
| **20** | `(10.16, 25.40)` | `1.70 × 1.70 mm` | circle | 1.00 mm |
| **21** | `(12.70, 25.40)` | `1.70 × 1.70 mm` | circle | 1.00 mm |
| **22** | `(15.24, 25.40)` | `1.70 × 1.70 mm` | circle | 1.00 mm |
| **23** | `(17.78, 25.40)` | `1.70 × 1.70 mm` | circle | 1.00 mm |
| **24** | `(20.32, 25.40)` | `1.70 × 1.70 mm` | circle | 1.00 mm |
| **25** | `(22.86, 25.40)` | `1.70 × 1.70 mm` | circle | 1.00 mm |
| **26** | `(25.40, 25.40)` | `1.70 × 1.70 mm` | circle | 1.00 mm |
| **27** | `(27.94, 25.40)` | `1.70 × 1.70 mm` | circle | 1.00 mm |
| **28** | `(30.48, 25.40)` | `1.70 × 1.70 mm` | circle | 1.00 mm |
| **29** | `(33.02, 25.40)` | `1.70 × 1.70 mm` | circle | 1.00 mm |
| **30** | `(35.56, 25.40)` | `1.70 × 1.70 mm` | circle | 1.00 mm |

### `U2` - Digispark_ATtiny85 (`FallSensor:Digispark_9Pin_RightAngle`)
- **Physical Dimensions**: `26.50 mm × 19.00 mm` (Production Rev 3: 17.5×19.0mm body + 9.0×12.0mm USB tongue)
- **Placement on PCB**: `X = 75.92 mm`, `Y = 119.25 mm`, Rotation = `0.0°` (Layer: F.Cu)
- **Total Pads**: 9 (thru_hole, drill 1.016 mm, pad 1.88 mm)
| Pad # | Function / Signal | Net Name | Local Offset (X, Y) | Board Coord (X, Y) | Pad Shape |
|---|---|---|---|---|---|
| **1** | P5 (Reset) | `unconnected-(U2-P5/RESET-Pad1)` | `(7.00, -7.45)` | `(82.92, 111.80)` | rect |
| **2** | P4 (MIC_SIG) | `Net-(U2-P4)` | `(7.00, -4.91)` | `(82.92, 114.34)` | circle |
| **3** | P3 (USB D+ / NC) | `unconnected-(U2-P3-Pad3)` | `(7.00, -2.37)` | `(82.92, 116.88)` | circle |
| **4** | P2 (PIR_WAKE) | `/PIR_WAKE` | `(7.00, 0.17)` | `(82.92, 119.42)` | circle |
| **5** | P1 (PIR_SIG) | `Net-(PIR1-OUT)` | `(7.00, 2.71)` | `(82.92, 121.96)` | circle |
| **6** | P0 (MIC_WAKE) | `/MIC_WAKE` | `(7.00, 5.25)` | `(82.92, 124.50)` | circle |
| **7** | GND (Ground) | `GND` | `(-3.29, 7.75)` | `(72.63, 127.00)` | circle |
| **8** | VIN (unconnected)| `unconnected-(U2-VIN-Pad8)` | `(-0.75, 7.75)` | `(75.17, 127.00)` | circle |
| **9** | 5V (+3V3 Rail) | `+3V3` | `(-5.83, 7.75)` | `(70.09, 127.00)` | rect |

### `U3` - MT3608_Module (`FallSensor:MT3608_Module`)
- **Physical Dimensions**: `36.00 mm × 17.00 mm` (Silkscreen Envelope: `X` in [74.00, 110.00] mm, `Y` in [51.00, 68.00] mm)
- **Placement on PCB**: `X = 77.25 mm`, `Y = 55.70 mm`, Rotation = `0.0°` (Layer: F.Cu)
- **Total Pads**: 4 (thru_hole, drill 1.20 mm, pad 2.00 mm)
| Pad # | Signal / Function | Net Name | Local Offset (X, Y) | Board Coord (X, Y) | Pad Shape | Hole Drill |
|---|---|---|---|---|---|---|
| **1** | VIN+ (Battery Boost In) | `Net-(U3-VIN+)` | `(0.00, 7.60)` | `(77.25, 63.30)` | rect | 1.20 mm |
| **2** | VIN- (Ground Return) | `GND` | `(0.00, 0.00)` | `(77.25, 55.70)` | circle | 1.20 mm |
| **3** | VOUT+ (+5V System Rail) | `+5V` | `(29.50, 7.60)` | `(106.75, 63.30)` | circle | 1.20 mm |
| **4** | VOUT- (Ground Return) | `GND` | `(29.50, 0.00)` | `(106.75, 55.70)` | circle | 1.20 mm |

### `U4` - TP4056_Module (`FallSensor:TP4056_Module`)
- **Physical Dimensions**: `17.00 mm × 27.00 mm` (Production Direct Standoff Mount, 14.0mm header span)
- **Placement on PCB**: `X = 76.00 mm`, `Y = 103.00 mm`, Rotation = `90.0°` (Layer: F.Cu)
- **Total Pads**: 4 (thru_hole, drill 1.00 mm, pad 1.70 mm)
| Pad # | Signal / Function | Net Name | Local Offset (X, Y) | Board Coord (X, Y) | Pad Shape |
|---|---|---|---|---|---|
| **3** | OUT+ (Positive Load Out) | `Net-(U4-OUT+)` | `(7.00, 0.00)` | `(76.00, 96.00)` | rect |
| **1** | B+ (Battery Positive) | `Net-(BT1-Pin_2)` | `(4.46, 0.00)` | `(76.00, 98.54)` | circle |
| **2** | B- (Battery Negative) | `Net-(BT1-Pin_1)` | `(-4.46, 0.00)` | `(76.00, 107.46)` | circle |
| **4** | OUT- (System Ground) | `GND` | `(-7.00, 0.00)` | `(76.00, 110.00)` | circle |

### `U5` - LM393_Sound_Module (`FallSensor:LM393_Sound_Module`)
- **Physical Dimensions**: `36.00 mm × 15.00 mm` (clean rectangle without potentiometer overhang)
- **Placement on PCB**: `X = 115.50 mm`, `Y = 76.81 mm`, Rotation = `90.0°` (Layer: F.Cu)
- **Acoustic Center of Electret Capsule**: `X = 142.50 mm`, `Y = 73.00 mm` — *Collinear on unified aperture axis $X = 142.50\text{ mm}$*
- **Total Pads**: 4 (thru_hole)
| Pad # | Local Offset (X, Y) | Pad Size (W × H) | Pad Shape | Hole Drill |
|---|---|---|---|---|
| **1** | `(0.00, 0.00)` | `1.70 × 1.70 mm` | rect | 1.00 mm |
| **2** | `(2.54, 0.00)` | `1.70 × 1.70 mm` | circle | 1.00 mm |
| **3** | `(5.08, 0.00)` | `1.70 × 1.70 mm` | circle | 1.00 mm |
| **4** | `(7.62, 0.00)` | `1.70 × 1.70 mm` | circle | 1.00 mm |

### `U6` - LoadSwitch_DBVT (Dual Strategy: Prototype 2.54mm THT Header vs Production SOT-23-6 SMD)

> **Design Note**: To facilitate prototyping and hand-assembly without microscope SMD soldering equipment, the current prototype board accommodates a **2.54mm Through-Hole (THT) daughterboard socket**. The ultra-compact **SOT-23-6 SMD footprint** is permanently preserved in the library (`FallSensor.pretty/SOT-23-6.kicad_mod`) for the next-generation fully automated SMD production iteration.

#### Option A: Production SMD Iteration (`FallSensor:SOT-23-6` / `Package_TO_SOT_SMD:SOT-23-6`)
- **Package Type**: Surface Mount (SMD 6-lead SOT-23)
- **Physical Dimensions**: `2.90 mm × 2.80 mm` (Courtyard: `4.10 mm × 3.40 mm`)
- **Lead Pitch**: `0.95 mm`
- **Pads**: 6 (smd roundrect `1.32 × 0.60 mm`)
- **Library Location**: Saved in `FallSensor.pretty/SOT-23-6.kicad_mod`

| Pad # | Function | Net | Description |
|---|---|---|---|
| **1** | VIN | `+5V` | 5V supply input from MT3608 boost converter |
| **2** | GND | `GND` | Ground return |
| **3** | ON / EN | `/RADAR_EN` | Active-high enable from ESP32 GPIO27 |
| **4** | GND | `GND` | Thermal ground return |
| **5** | GND | `GND` | Thermal ground return |
| **6** | VOUT | `Net-(RADAR1-VIN)` | Switched 5V power output to C1001 Radar module |

#### Option B: Prototype Hand-Assembly Daughterboard Socket (`FallSensor:PinHeader_2x03_P2.54mm_Vertical` / `FallSensor:DIP-6_W7.62mm`)
- **Package Type**: Through-Hole Technology (THT 2.54mm pin header / DIP-6 socket)
- **Physical Dimensions**: `5.08 mm × 7.62 mm` (2 rows of 3 pins)
- **Pin Pitch**: `2.54 mm (0.1")`
- **Row Spacing**: `2.54 mm` (Pin Header) or `7.62 mm (300 mil)` (DIP-6 Socket)
- **Mounting**: Hand-soldered female/male header socket accepting a plug-in SOT-23-to-DIP daughterboard breakout
- **Library Location**: Saved in `FallSensor.pretty/PinHeader_2x03_P2.54mm_Vertical.kicad_mod` and `FallSensor.pretty/DIP-6_W7.62mm.kicad_mod`

### `U7` - Buck Converter (`FallSensor:LM2596_Module`)
- **Physical Dimensions**: `43.18 mm × 21.08 mm` (Silkscreen Envelope: `X` in [50.53, 71.62] mm, `Y` in [50.66, 93.84] mm)
- **Placement on PCB**: `X = 68.50 mm`, `Y = 52.50 mm`, Rotation = `-90.0°` (Layer: F.Cu)
- **Total Pads**: 4 (thru_hole, drill 1.50 mm, pad 3.00 mm)
| Pad # | Signal / Function | Net Name | Board Coord (X, Y) | Pad Shape | Hole Drill |
|---|---|---|---|---|---|
| **1** | IN+ (+5V Power In) | `+5V` | `(69.65, 52.50)` | rect | 1.50 mm |
| **2** | IN- (Ground Return) | `GND` | `(52.50, 52.50)` | circle | 1.50 mm |
| **3** | OUT+ (+3V3 Regulated Out)| `+3V3` | `(69.65, 92.00)` | circle | 1.50 mm |
| **4** | OUT- (Ground Return) | `GND` | `(52.50, 92.00)` | circle | 1.50 mm |

