# 🖨️ Fall Sensor System - Wall-Mount 3D Printed Enclosure

This directory contains the complete **3D CAD engineering stream** for the Wall-Mounted Enclosure of the Fall Sensor System.

---

## 📁 Files in this Directory

| File | Type | Description |
|---|---|---|
| [`fall_sensor_enclosure_base.stl`](fall_sensor_enclosure_base.stl) | 3D Mesh (STL) | **Base Mount**: Internal PCB standoffs, 4 corner screw bosses, 2 rear keyholes, USB-C & Power switch ports. |
| [`fall_sensor_enclosure_lid.stl`](fall_sensor_enclosure_lid.stl) | 3D Mesh (STL) | **Front Cover**: PIR dome opening, Radar RF window, Mic port, Fall LED hole, Sync button pinhole. |
| [`fall_sensor_enclosure.scad`](fall_sensor_enclosure.scad) | OpenSCAD Source | **Parametric CAD model**: Fully customizable wall thickness, standoff height, and aperture sizes. |
| [`fall_sensor_enclosure.blend`](fall_sensor_enclosure.blend) | Blender CAD | **Master Blender 2.91+ CAD project**: Contains full scene, lighting, materials, and export pipeline. |
| [`fall_sensor_enclosure_studio.png`](fall_sensor_enclosure_studio.png) | High-Res Render | 3D perspective rendering of the base and lid side-by-side. |
| [`fall_sensor_enclosure_wallmount.png`](fall_sensor_enclosure_wallmount.png) | High-Res Render | Rear perspective view showing the wall-mounting keyhole slots. |

---

## 📐 Enclosure Dimensions & Mechanical Specifications

* **External Dimensions:** `106.8 mm (Width) × 86.8 mm (Depth) × 32.4 mm (Total Height)`
* **Internal Cavity:** `102.0 mm × 82.0 mm × 27.6 mm` (fits standard $100 \times 80\text{ mm}$ PCB with $1.0\text{ mm}$ expansion margin).
* **Wall Thickness:** `2.4 mm` (high structural rigidity and impact resistance).
* **Base Height:** `13.0 mm` | **Lid Height:** `19.4 mm` with a `1.8 mm` interlocking alignment lip.

---

## 🔍 Sensor Openings & Port Map

The enclosure lid and walls feature precision apertures matched to the hardware footprint:

```
+-------------------------------------------------------------------------+
|                                                                         |
|                          [ PIR Dome Aperture ]                          |
|                             (Dia: 12.0 mm)                              |
|                                                                         |
|   [ Mic Acoustic Port ]                                                 |
|       (Dia: 3.0 mm)                                                     |
|                                                                         |
|                                               [ Status Fall LED ]       |
|                                                  (Dia: 3.2 mm)          |
|                                                                         |
|                                            [ C1001 Radar RF Window ]    |
|   [ Sync Button Pinhole ]                       (26 x 26 mm Recess,     |
|        (Dia: 3.5 mm)                            1.0 mm Thin-Wall)       |
|                                                                         |
+-------------------------------------------------------------------------+
     |                                                       |
 [Power Switch]                                          [USB-C Port]
 (Left Wall: 9.5x5.0mm)                             (Bottom Wall: 11x4.8mm)
```

1. **AM312 PIR Fresnel Dome (`Dia 12.0 mm`):** Extends the hemispherical lens through the front face for an unobstructed $100^\circ$ passive infrared motion cone.
2. **C1001 Radar RF Transmission Window (`26.0 × 26.0 mm`):** Recessed to a **$1.0\text{ mm}$ thin wall**. Millimeter-wave radar (24GHz / 60GHz) passes cleanly through thin plastic with negligible attenuation.
3. **Sound Sensor Acoustic Inlet (`Dia 3.0 mm`):** Positioned directly over the LM393 electret microphone capsule to allow sound waves from a floor "THUD" to reach the diaphragm unimpeded.
4. **Status / Fall Alarm LED (`Dia 3.2 mm`):** Sits flush with a standard 3mm LED or accepts a standard acrylic light pipe for high visibility.
5. **Sync Button Pinhole (`Dia 3.5 mm`):** Allows triggering the WiFi/BLE sync tactile switch using a paperclip or stylus without opening the box.
6. **TP4056 USB-C Charging Cutout (`11.0 × 4.8 mm`):** Allows plugging in standard USB-C cables for battery recharging or continuous wall power.
7. **Power Switch Slot (`9.5 × 5.0 mm`):** Cutout on the left edge for the main power slide/toggle switch.

---

## 🧱 Wall Mounting Guidelines (9-Foot Ceiling Height)

* **Mounting Method:** Two rear **Keyhole Hanging Slots** spaced **$50.0\text{ mm}$ apart**.
  * Entry hole: $\varnothing 8.5\text{ mm}$ (fits drywall screw heads up to $\varnothing 8\text{ mm}$).
  * Slide slot: $4.5\text{ mm}$ wide (accepts standard #6, #8, M3.5, or M4 screws).
  * Retaining lip: $1.4\text{ mm}$ recessed shelf for secure, anti-shake retention.
* **Wall Installation:**
  1. Drive two screws into the wall at the desired room height ($2.4\text{ m} - 2.7\text{ m}$ / 8 to 9 feet), spaced exactly **$50.0\text{ mm}$ vertically or horizontally**, leaving $\approx 2.5\text{ mm}$ of screw head exposed.
  2. Slide the enclosure onto the screw heads and pull downwards to lock into the keyholes.
  3. The unit can be lifted off in seconds for inspection or portable charging.

---

## 🖨️ 3D Printing Recommended Slicer Settings

| Parameter | Recommended Value | Notes |
|---|---|---|
| **Filament Material** | **PETG** or **ABS / ASA** (PLA for prototypes) | PETG provides high UV and thermal resistance; PLA works fine indoors. |
| **Layer Height** | `0.20 mm` | Good balance of printing speed and layer adhesion. |
| **Perimeters / Wall Loops** | `4 loops` ($1.6\text{ mm}$) | Enhances screw boss strength and prevents delamination. |
| **Top & Bottom Layers** | `5 solid layers` ($1.0\text{ mm}$) | Guarantees watertightness and rigidity. |
| **Infill Density & Pattern** | `20% - 25% Gyroid` or `Grid` | Gyroid offers uniform strength in all directions. |
| **Supports** | **Only on Base build plate** | Supports needed only inside the USB-C and power switch horizontal bridges. |
| **Build Orientation** | **Base:** Bottom face down on bed<br>**Lid:** Front face down on bed | No supports needed on the lid front face! |

---

## 🔩 Hardware Bill of Materials (Assembly Screws)

* **PCB Mounting:** 4x `M3 × 6 mm` pan-head self-tapping screws (or `M3 × 5 mm` machine screws with brass heat-set inserts).
* **Enclosure Lid Closure:** 4x `M3 × 16 mm` countersunk screws.
* **Wall Screws:** 2x Standard drywall screws (#6 or #8 with plastic expansion anchors).
