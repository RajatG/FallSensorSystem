# 🖨️ Fall Sensor System - Wall-Mount 3D Printed Enclosure

This directory contains the complete **3D CAD engineering stream** for the Wall-Mounted Enclosure of the Fall Sensor System.

---

## 📁 Files in this Directory

| File | Type | Description |
|---|---|---|
| [`fall_sensor_enclosure_base.stl`](fall_sensor_enclosure_base.stl) | 3D Mesh (STL) | **Base Mount (v2.1)**: Integrated 79.5mm 18650 battery compartment with wire notch, retaining end-wall, open PIR alcove, 5mm PCB shelf posts, 4 corner screw bosses, rear wall-mount keyholes, USB-C port, and side ventilation louvers. |
| [`fall_sensor_enclosure_lid.stl`](fall_sensor_enclosure_lid.stl) | 3D Mesh (STL) | **Front Cover (v2.1)**: Balanced square profile with 4 corner screw guide pillars, 4 downward PCB clamping tabs (3.9mm), PIR dome opening, Radar RF thin window, Mic port, Fall LED hole, Sync button pinhole, and side ventilation. |
| [`fall_sensor_enclosure_assembled_hero.png`](fall_sensor_enclosure_assembled_hero.png) | High-Res Render | Assembled square enclosure hero view in locked high-contrast studio scene. |
| [`fall_sensor_enclosure_exploded.png`](fall_sensor_enclosure_exploded.png) | High-Res Render | Exploded assembly view showing floating lid with visible downward clamp tabs, base alignment, and internal features. |
| [`fall_sensor_enclosure_studio.png`](fall_sensor_enclosure_studio.png) | High-Res Render | Studio side-by-side open view showing both internal cavities (battery bay and shelf posts on left; clamp tabs and radar pocket on right). |
| [`fall_sensor_enclosure_wallmount.png`](fall_sensor_enclosure_wallmount.png) | High-Res Render | Rear perspective view showing the 50mm spaced wall-mounting keyhole slots. |
| [`fall_sensor_pcb_dummy.stl`](fall_sensor_pcb_dummy.stl) | 3D Mesh (STL) | **1:1 Scale Test-Fit PCB ($100.00 \times 80.00 \times 1.51\text{ mm}$)**: Exact 3D mesh exported directly from KiCad 10 with all 186 through-hole pin and via drill cutouts (ESP32, ATtiny85, TP4056, C1001 Radar, passives, etc.) for physical hole-alignment and base cavity test-fitting. |
| [`fall_sensor_enclosure.blend`](fall_sensor_enclosure.blend) | Blender CAD | **Master Blender 2.91+ CAD project**: Exact parametric Boolean geometry, Cycles lighting, materials, and automated multi-view render pipeline. |

---

## 📐 Enclosure Dimensions & Mechanical Specifications (v2.1 Balanced Square)

* **External Dimensions:** `116.8 mm (Width) × 110.8 mm (Depth) × 31.4 mm (Total Height)`
* **Form Factor Aspect Ratio:** `1.05 : 1` — **Balanced modern square form factor**.
* **Base Height:** `13.0 mm` (Floor thickness: `2.4 mm`).
* **Lid Height:** `18.4 mm` with an interlocking `1.8 mm` perimeter alignment lip (Ceiling thickness: `2.4 mm`).
* **Total Enclosure Assembled Height:** `31.4 mm`.
* **Outer Wall Thickness:** `2.4 mm` throughout for high structural rigidity and impact resistance.
* **Internal Battery Compartment:** Dedicated `79.5 mm (W) × 22.0 mm (D) × 26.6 mm (H)` cradle on the left with a rigid vertical retaining end-wall at $X = +23.5\text{ mm}$ and a $8.0 \times 6.0\text{ mm}$ wire pass-through notch, cleanly fitting standard 18650 battery holders ($75\text{–}79\text{ mm}$).
* **Open PIR Sensor Alcove:** The region to the right of the battery retaining wall ($X = +23.5$ to $+56.0\text{ mm}$, width $32.5\text{ mm}$) is **100% open** to the main PCB cavity, allowing the AM312 PIR sensor to extend freely without any wall interference.
* **Internal PCB Compartment:** `102.0 mm × 82.0 mm` pocket providing a snug `1.0 mm` perimeter clearance around the standard $100 \times 80\text{ mm}$ PCB.
* **Radar RF Isolation Chamber:** Dedicated $10.0\text{ mm}$ right-side expansion chamber ($X = +45.0$ to $+56.0\text{ mm}$) providing complete dielectric isolation and free-air clearance for the overhanging C1001 60GHz radar antenna patches.

---

## 🔒 PCB Clamping Architecture (Zero-Screw Sandwich Clamp)

The enclosure utilizes a **zero-screw perimeter clamping architecture**, eliminating the need for dedicated screw holes through the PCB and maximizing usable copper routing area:

```
  ┌─────────────────────────────────────────────────────────┐  Lid Ceiling (Z = 29.0 mm)
  │                     Lid Cavity                          │
  │     [Headroom: 20.0 mm clear space above PCB]           │
  │                                                         │
  │   [4x PCB Downward Clamp Tabs]                          │  Lid Rim (Z = 13.0 mm)
  │   └── Depth: 3.9 mm ───┐                                │
  └───┬────────────────────┼────────────────────────────────┘
      ▼                    ▼  (Snug Downward Clamping)
  ═══════════════════════════════════════════════════════════  PCB Top Surface (Z = 9.0 mm)
              PCB (FR4 Core, Thickness = 1.6 mm)
  ═══════════════════════════════════════════════════════════  PCB Bottom Surface (Z = 7.4 mm)
      ▲                    ▲  (Solid Upward Support)
  ────┴────────────────────┴─────────────────────────────────
  │   └── 4x Perimeter Shelf Posts (Height: 5.0 mm)         │
  │                                                         │
  │   [Solder Clearance: 5.0 mm air gap to floor]           │
  └─────────────────────────────────────────────────────────┘  Base Floor (Z = 0.0 to 2.4 mm)
```

1. **Underside Support (Base Shelf Posts):**
   * 4 monolithic perimeter shelf posts ($4.0 \times 4.0\text{ mm}$, height `5.0 mm`) molded directly into the base floor.
   * Located at certified copper-free and pin-free keepout zones: Left `(-53.5, -43.0)`, Right `(+43.5, -21.0)`, Bottom `(+23.0, -50.5)`, Top `(+23.0, +26.5)`.
   * Provides a generous `5.0 mm` air gap above the floor, completely clear of all through-hole solder pins and joints.
2. **Top Clamping (Lid Downward Tabs):**
   * 4 monolithic downward clamp tabs ($4.0 \times 4.0\text{ mm}$, height `3.9 mm`) molded into the lid ceiling directly over the base shelf posts.
   * Strategically positioned in certified open keepout zones completely clear of all headers, modules, and components (Left between SW2 & BT1; Right between D1 & RADAR1; Bottom between SW1 & RADAR1; Top between C8 & PIR1).
   * When the 4 lid screws are fastened, the tabs apply a firm `0.1 mm` compression onto the bare PCB perimeter, locking the board rigidly with **zero vertical rattle** and **zero lateral play**.

---

## 🔍 Sensor Openings & Port Map

The enclosure apertures match the physical PCB component footprint coordinates down to the sub-millimeter:

```
+-------------------------------------------------------------------------+
|      [ 18650 Battery Cradle (79.5mm) ]       |   [ Open PIR Alcove ]    |
+----------------------------------------------+--------------------------+
|                                              [ PIR Dome Aperture ]      |
|                                                 (Dia: 12.0 mm)          |
|                                                                         |
|                       [ Mic Acoustic Port ]                             |
|                           (Dia: 3.0 mm)                                 |
|                                              [ Status Fall LED ]        |
|    [USB-C Port]                                 (Dia: 3.2 mm)           |
|   (11.0x4.8mm)                                                          |
|                                              [ C1001 Radar RF Window ]  |
|   (Solid Left Wall,     [ Sync Button ]           (Internal Pocket,     |
|    Internal Jumper)      (Dia: 3.5 mm)             1.0 mm Membrane)     |
+-------------------------------------------------------------------------+
        ▲                                              ▲
    LEFT WALL                                      RIGHT SIDE
```

| Aperture / Port | Location / Face | Coordinates `(ex, ey)` | Dimensions | Matching Hardware Component |
|---|---|:---:|---|---|
| **PIR Fresnel Dome** | Top Lid Face | `(+34.50, +19.75) mm` | $\varnothing 12.0\text{ mm}$ round hole | `PIR1` (AM312 PIR motion sensor lens, $100^\circ$ cone) |
| **LM393 Mic Sound Port** | Top Lid Face | `(+10.50, +1.19) mm` | $\varnothing 3.0\text{ mm}$ round hole | `U5` (Electret microphone capsule acoustic inlet) |
| **C1001 Radar RF Window** | Inside Lid Ceiling | `(+41.50, -34.00) mm` | $22.0 \times 22.0\text{ mm}$ pocket ($1.0\text{ mm}$ membrane) | `RADAR1` (RF transparent window over 60GHz antenna) |
| **Status / Fall Alarm LED** | Top Lid Face | `(+35.23, -11.00) mm` | $\varnothing 3.2\text{ mm}$ round hole | `D1` (3mm through-hole LED / light-pipe opening) |
| **Sync / Reset Button** | Top Lid Face | `(+2.25, -43.25) mm` | $\varnothing 3.5\text{ mm}$ pinhole | `SW1` (6x6x8mm tactile push button access via pin) |
| **USB-C Charging Cutout** | Left Base Wall | `(-58.40, -25.00) mm` | $11.0 \times 4.8\text{ mm}$ slot ($Z = 10.6\text{ mm}$) | `U4` (TP4056 Type-C battery charger receptacle) |
| **Power Switch** | Internal on PCB | *N/A* | *No external cutout* (Solid wall) | `SW2` (Standard 2.54mm header pin jumper cap / shunt) |
| **Cooling Vents** | Right Wall | $Y \in [-15, +15]\text{ mm}$ | 6x vertical slots ($1.6 \times 7.0\text{ mm}$) | Convective thermal dissipation for MT3608 & TP4056 |

---

## 🧱 Wall Mounting Guidelines

* **Mounting Method:** Two rear **Keyhole Hanging Slots** spaced **$50.0\text{ mm}$ apart**.
  * Entry hole: $\varnothing 8.5\text{ mm}$ (fits standard drywall screw heads up to $\varnothing 8.0\text{ mm}$).
  * Slide slot: $4.5\text{ mm}$ wide (accepts standard #6, #8, M3.5, or M4 screws).
  * Retaining lip: $1.4\text{ mm}$ recessed shelf for anti-shake retention.
* **Wall Installation:**
  1. Drive two screws into the wall at standard wall height ($2.4\text{ m} - 2.7\text{ m}$ / 8 to 9 feet), spaced **$50.0\text{ mm}$ vertically**, leaving $\approx 2.5\text{ mm}$ of screw head exposed.
  2. Align the keyholes with the screw heads and push downwards to lock into place.
  3. The unit can be unhooked in seconds for USB-C recharging or battery replacement.

---

## 🖨️ 3D Printing Recommended Slicer Settings

| Slicer Setting | Recommended Value | Notes |
|---|---|---|
| **Filament Material** | **PETG** (or ABS/ASA; PLA for indoor prototypes) | PETG provides superior heat resistance and impact toughness. |
| **Layer Height** | `0.20 mm` (Quality/Standard) | Optimum balance of fine feature resolution and layer strength. |
| **Wall Loops / Perimeters** | `4 loops` ($1.6\text{ mm}$ thickness) | Essential for solid screw boss pillars and durable corner threads. |
| **Top & Bottom Solid Layers** | `5 layers` ($1.0\text{ mm}$) | Ensures watertight ceiling and rigid bottom base plate. |
| **Infill Density & Pattern** | `20% - 25% Gyroid` or `Grid` | Gyroid provides isotropic structural strength. |
| **Supports** | **Minimal (Base build plate only)** | Only a small support tree inside the horizontal USB-C bridge. |
| **Build Plate Orientation** | **Base:** Bottom face flat on bed<br>**Lid:** Top face flat on bed | **Zero supports required on the lid outer face!** |

---

## 🔩 Hardware Bill of Materials (Assembly Screws)

| Application | Quantity | Screw Specification | Recommended Product / Notes |
|---|---|---|---|
| **Enclosure Lid Closure** | **4x** | **`M3 × 25 mm` Hex Allen CSK** (Countersunk Flat Head) | [EasyMech M3 × 25mm Hex CSK](https://robu.in/product/ntl-easymech-m3-x-25mm-hex-allen-csk-high-tensile109-black-oxide-screw-dia-3mm-length-25mm). Passes through 18.4mm lid pillars and grips 6.6mm into base bosses. Sits flush with top face. |
| **PCB Mounting** | **0x** | *None required* | PCB is rigidly clamped between the base shelf posts and lid downward tabs. |
| **Wall Mounting** | **2x** | Standard drywall screws (#6 or #8) | Head diameter $\le 8.0\text{ mm}$, shaft $\le 4.2\text{ mm}$, with wall anchors. |
