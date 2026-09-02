// ====================================================================
// Fall Sensor System - Parametric Wall-Mount 3D Printed Enclosure
// Version: v1.1 — Corrected aperture positions, ventilation, clean lid
// Compatible with: OpenSCAD / FreeCAD / Bambu Studio / Cura / PrusaSlicer
// ====================================================================

// [PCB & Clearances]
pcb_width       = 100.0;   // PCB X dimension (mm)
pcb_depth       = 80.0;    // PCB Y dimension (mm)
pcb_thickness   = 1.6;     // Standard 2-layer FR4 thickness
pcb_clearance   = 1.0;     // Clearance around PCB perimeter (mm)

// [Enclosure Walls & Heights]
wall            = 2.4;     // Outer wall thickness (mm)
floor_thick     = 2.4;     // Base bottom thickness (mm)
lid_thick       = 2.4;     // Top lid face thickness (mm)
standoff_height = 5.0;     // Height of PCB standoffs above base floor (mm)
comp_height     = 20.0;    // Max component clearance above PCB (mm)
corner_radius   = 4.0;     // Outer rounded corner radius (mm)

// [Calculated Dimensions]
inner_w = pcb_width + 2 * pcb_clearance;  // 102.0 mm
inner_d = pcb_depth + 2 * pcb_clearance;  // 82.0 mm
outer_w = inner_w + 2 * wall;             // 106.8 mm
outer_d = inner_d + 2 * wall;             // 86.8 mm
base_h  = floor_thick + standoff_height + pcb_thickness + 4.0; // 13.0 mm
lid_h   = comp_height - 4.0 + lid_thick;  // 18.4 mm
total_h = base_h + lid_h;                 // 31.4 mm

// =================================================================
// [Sensor Port Coordinates — CORRECTED from actual KiCad PCB layout]
// Origin: PCB bottom-left corner (KiCad X=50, Y=130)
// PCB_rel_x = KiCad_x - 50;  PCB_rel_y = 130 - KiCad_y
// =================================================================

// 1. AM312 PIR Fresnel Dome Aperture
//    KiCad: (125.5, 58.25) → PCB_rel: (75.5, 71.75)
pir_x = 75.5;
pir_y = 71.75;
pir_dia = 12.0;   // 10mm dome + 2mm clearance

// 2. C1001 60GHz Radar RF Window
//    KiCad center: ~(150, 119) → PCB_rel: (100, 11)
//    Radar module is 25.4x25.4mm, centered at PCB_rel (87.5, 11.0)
//    But it overhangs the right edge. Antenna center ≈ PCB_rel (90, 15)
radar_x = 90.0;
radar_y = 15.0;
radar_w = 26.0;
radar_d = 26.0;

// 3. LM393 Sound Sensor Acoustic Port (Microphone Hole)
//    KiCad: (115.5, 76.81) → PCB_rel: (65.5, 53.2)
mic_x = 65.5;
mic_y = 53.2;
mic_dia = 3.0;

// 4. Status Fall Alarm LED Hole (3mm LED)
//    KiCad: (140.23, 89.0) → PCB_rel: (90.2, 41.0)
led_x = 90.2;
led_y = 41.0;
led_dia = 3.2;

// 5. Sync Tactile Button Access Pinhole
//    KiCad: (107.25, 121.25) → PCB_rel: (57.25, 8.75)
btn_x = 57.25;
btn_y = 8.75;
btn_dia = 3.5;

// 6. TP4056 USB-C Charging Port Slot (Bottom wall: Y=0 edge)
//    KiCad: (76, 130) → PCB_rel: (26, 0) — on the Y=0 (bottom) edge
usb_x = 26.0;
usb_w = 11.0;
usb_h = 4.8;

// 7. SW2 Power Switch Slot (Left wall: X=0 edge)
//    KiCad: (50, 114.5) → PCB_rel: (0, 15.5) — on the X=0 (left) edge
sw_y = 15.5;
sw_w = 9.5;
sw_h = 5.0;

// [Wall Mount Keyholes]
keyhole_spacing = 50.0;
kh_large_dia = 8.5;
kh_small_dia = 4.5;

// [Ventilation]
vent_slot_w = 1.5;     // Slot width
vent_slot_h = 8.0;     // Slot height
vent_slot_spacing = 4.0;
vent_num_slots = 6;

// [Render Selector]
part = "both"; // ["both", "base", "lid", "assembled"]

$fn = 40;

// --- Helper Modules ---
module rounded_box(w, d, h, r) {
    hull() {
        translate([-w/2 + r, -d/2 + r, 0]) cylinder(r=r, h=h);
        translate([ w/2 - r, -d/2 + r, 0]) cylinder(r=r, h=h);
        translate([-w/2 + r,  d/2 - r, 0]) cylinder(r=r, h=h);
        translate([ w/2 - r,  d/2 - r, 0]) cylinder(r=r, h=h);
    }
}

module keyhole() {
    union() {
        cylinder(d=kh_large_dia, h=floor_thick + 1, center=false);
        translate([0, 4.0, 0]) cylinder(d=kh_small_dia, h=floor_thick + 1, center=false);
        translate([-kh_small_dia/2, 0, 0]) cube([kh_small_dia, 4.0, floor_thick + 1]);
        translate([0, 4.0, 1.2]) cylinder(d=kh_large_dia, h=floor_thick, center=false);
    }
}

module vent_slots(count, slot_w, slot_h, wall_t) {
    total_span = (count - 1) * vent_slot_spacing;
    for (i = [0:count-1]) {
        translate([0, -total_span/2 + i * vent_slot_spacing, 0])
            cube([wall_t + 2, slot_w, slot_h], center=true);
    }
}

// --- Base Part ---
module enclosure_base() {
    difference() {
        // Outer Shell
        rounded_box(outer_w, outer_d, base_h, corner_radius);

        // Inner Cavity
        translate([0, 0, floor_thick])
            rounded_box(inner_w, inner_d, base_h, corner_radius - 1);

        // Rear Wall-Mount Keyholes in bottom floor
        translate([0, -keyhole_spacing/2, -0.5]) keyhole();
        translate([0,  keyhole_spacing/2, -0.5]) keyhole();

        // USB-C Cutout on bottom wall (Y = -outer_d/2, PCB Y=0 edge)
        translate([-inner_w/2 + pcb_clearance + usb_x, -outer_d/2, floor_thick + standoff_height + pcb_thickness])
            cube([usb_w, wall*2 + 2, usb_h], center=true);

        // Power Switch Cutout on left wall (X = -outer_w/2, PCB X=0 edge)
        translate([-outer_w/2, -inner_d/2 + pcb_clearance + sw_y, floor_thick + standoff_height + pcb_thickness + 1.0])
            cube([wall*2 + 2, sw_w, sw_h], center=true);

        // Ventilation Slots — Right wall (X = +outer_w/2)
        // Positioned at mid-height of the base for airflow over ESP32 & MT3608
        translate([outer_w/2, 0, floor_thick + base_h/2])
            vent_slots(vent_num_slots, vent_slot_w, vent_slot_h, wall);
    }

    // 4 PCB Standoffs
    for (sx = [-pcb_width/2 + 4.0, pcb_width/2 - 4.0]) {
        for (sy = [-pcb_depth/2 + 4.0, pcb_depth/2 - 4.0]) {
            translate([sx, sy, floor_thick]) {
                difference() {
                    cylinder(d=6.5, h=standoff_height);
                    translate([0, 0, 0.5]) cylinder(d=2.6, h=standoff_height + 1);
                }
            }
        }
    }

    // 4 Corner Screw Bosses for Lid
    boss_x = outer_w/2 - 5.0;
    boss_y = outer_d/2 - 5.0;
    for (bx = [-boss_x, boss_x]) {
        for (by = [-boss_y, boss_y]) {
            translate([bx, by, floor_thick]) {
                difference() {
                    cylinder(d=7.0, h=base_h - floor_thick);
                    translate([0, 0, 1.0]) cylinder(d=2.8, h=base_h);
                }
            }
        }
    }
}

// --- Lid Part ---
module enclosure_lid() {
    difference() {
        union() {
            // Outer Shell
            rounded_box(outer_w, outer_d, lid_h, corner_radius);

            // Alignment Lip (steps into base cavity)
            translate([0, 0, -1.8])
                difference() {
                    rounded_box(inner_w - 0.5, inner_d - 0.5, 2.0, corner_radius - 1);
                    translate([0, 0, -0.5])
                        rounded_box(inner_w - 0.5 - 2*1.5, inner_d - 0.5 - 2*1.5, 3.0, corner_radius - 2);
                }
        }

        // Inner Cavity
        translate([0, 0, -2.0])
            rounded_box(inner_w, inner_d, lid_h - lid_thick + 2.0, corner_radius - 1);

        // 4 Corner Countersunk Screw Holes
        boss_x = outer_w/2 - 5.0;
        boss_y = outer_d/2 - 5.0;
        for (bx = [-boss_x, boss_x]) {
            for (by = [-boss_y, boss_y]) {
                translate([bx, by, -2.5]) cylinder(d=3.3, h=lid_h + 5);
                translate([bx, by, lid_h - 2.5]) cylinder(d1=3.3, d2=6.5, h=3.0);
            }
        }

        // === SENSOR & USER INTERFACE APERTURES ===
        // PCB Origin in centered coordinates (PCB bottom-left = (-inner_w/2+clearance, -inner_d/2+clearance))
        pcb_ox = -inner_w/2 + pcb_clearance;
        pcb_oy = -inner_d/2 + pcb_clearance;

        // 1. AM312 PIR Fresnel Dome Aperture (CORRECTED position)
        translate([pcb_ox + pir_x, pcb_oy + pir_y, lid_h - lid_thick - 1])
            cylinder(d=pir_dia, h=lid_thick + 3);

        // 2. C1001 Radar RF Window (Thin-wall transmission zone, 1.0mm thick)
        translate([pcb_ox + radar_x - radar_w/2, pcb_oy + radar_y - radar_d/2, lid_h - lid_thick + 1.0])
            cube([radar_w, radar_d, lid_thick]);

        // 3. Microphone Acoustic Inlet Port (CORRECTED position)
        translate([pcb_ox + mic_x, pcb_oy + mic_y, lid_h - lid_thick - 1])
            cylinder(d=mic_dia, h=lid_thick + 3);

        // 4. Status Fall Alarm LED Hole (CORRECTED position)
        translate([pcb_ox + led_x, pcb_oy + led_y, lid_h - lid_thick - 1])
            cylinder(d=led_dia, h=lid_thick + 3);

        // 5. Sync Tactile Button Access Pinhole (CORRECTED position)
        translate([pcb_ox + btn_x, pcb_oy + btn_y, lid_h - lid_thick - 1])
            cylinder(d=btn_dia, h=lid_thick + 3);

        // Ventilation Slots — Right wall of lid (matching base)
        translate([outer_w/2, 0, lid_h/2])
            vent_slots(vent_num_slots, vent_slot_w, vent_slot_h, wall);

        // Ventilation Slots — Left wall of lid (opposite side)
        translate([-outer_w/2, 0, lid_h/2])
            vent_slots(4, vent_slot_w, vent_slot_h, wall);
    }
}

// --- Render Layout ---
if (part == "both") {
    translate([-outer_w/2 - 10, 0, 0]) enclosure_base();
    translate([ outer_w/2 + 10, 0, 0]) enclosure_lid();
} else if (part == "base") {
    enclosure_base();
} else if (part == "lid") {
    enclosure_lid();
} else if (part == "assembled") {
    enclosure_base();
    translate([0, 0, base_h + lid_h]) rotate([180, 0, 0]) enclosure_lid();
}
