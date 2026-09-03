# 📄 Printable PDFs & Manufacturing Drawings

This directory contains the organized printable PDF packages for testing, assembly, and schematic review of the Fall Sensor PCB.

---

## 🌟 Essential Files (Root)

| File | Format | Description |
|---|:---:|---|
| **[`fall_sensor_pcb_front_and_back_A4.pdf`](fall_sensor_pcb_front_and_back_A4.pdf)** | **1:1 Vector PDF** | **Paper Testing Template**: Side-by-side Top and Bottom layers at exact 1:1 true CAD scale ($100.0 \times 80.0\text{ mm}$ board outlines) with precision 10.0 cm calibration ruler. |
| **[`fall_sensor_schematic_A4_printable.pdf`](fall_sensor_schematic_A4_printable.pdf)** | **A4 PDF** | **Printable Schematic**: Complete system schematic formatted to fit standard A4 paper for workbench reference. |
| **[`fall_sensor_pcb_front_and_back_A4.jpg`](fall_sensor_pcb_front_and_back_A4.jpg)** | High-Res Image | High-resolution 300 DPI preview of the 1:1 print sheet. |

---

## 📁 Subdirectories

### 1. `assembly/` — Fabrication & Component Placement
* **[`fall_sensor_pcb_top_assembly.pdf`](assembly/fall_sensor_pcb_top_assembly.pdf)**: Top layer silkscreen, component reference designators, and pin-1 markers for manual soldering.
* **[`fall_sensor_pcb_bottom_assembly.pdf`](assembly/fall_sensor_pcb_bottom_assembly.pdf)**: Bottom layer reference markings and test points.
* **[`fall_sensor_pcb_all_layers.pdf`](assembly/fall_sensor_pcb_all_layers.pdf)**: Complete multi-layer CAD drawing containing all copper and silkscreen layers.

### 2. `layers/` — Individual Copper Layers
* **[`fall_sensor_pcb_top_board_only.pdf`](layers/fall_sensor_pcb_top_board_only.pdf)**: Top copper traces (`F.Cu`), front silkscreen (`F.SilkS`), and board edge cuts (`Edge.Cuts`).
* **[`fall_sensor_pcb_bottom_board_only.pdf`](layers/fall_sensor_pcb_bottom_board_only.pdf)**: Bottom copper traces (`B.Cu`), bottom ground plane, and mirrored view for DIY toner-transfer or inspection.

### 3. `schematic/` — Full-Size Engineering Schematic
* **[`fall_sensor_schematic.pdf`](schematic/fall_sensor_schematic.pdf)**: Full-size standard A3 engineering schematic directly exported from KiCad 10 Eeschema.

---

> [!TIP]
> **Printing Instructions for 1:1 Accuracy:**
> When printing `fall_sensor_pcb_front_and_back_A4.pdf`, ensure your PDF viewer is set to **"Actual Size"** or **"Custom Scale: 100%"**. Never select "Fit to Printable Area". Verify accuracy using the 100 mm scale ruler at the bottom.
