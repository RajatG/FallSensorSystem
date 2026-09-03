// ====================================================================
// Fall Sensor System - Parametric Wall-Mount 3D Printed Enclosure
// Version: v2.0 — Square Profile (107x111mm) with Integrated 18650 Battery Bay
// Compatible with: OpenSCAD / FreeCAD / Bambu Studio / Cura / PrusaSlicer
// ====================================================================

// [PCB & Clearances]
pcb_width       = 100.0;   // PCB X dimension (mm)
pcb_depth       = 80.0;    // PCB Y dimension (mm)
pcb_thickness   = 1.6;     // Standard 2-layer FR4 thickness
pcb_clearance   = 1.0;     // Clearance around PCB perimeter (mm)

// [18650 Battery Bay Dimensions (Placed at Top)]
bat_bay_depth   = 22.0;    // Fits standard 21mm wide 18650 single-cell holder
divider_thick   = 2.0;     // Separation rib between battery and PCB
divider_height  = 12.0;    // Height of divider wall above floor
wire_notch_w    = 8.0;     // Wire pass-through notch for battery leads

// [Enclosure Walls & Heights]
wall            = 2.4;     // Outer wall thickness (mm)
floor_thick     = 2.4;     // Base bottom thickness (mm)
lid_thick       = 2.4;     // Top lid face thickness (mm)
standoff_height = 5.0;     // Height of PCB standoffs above base floor (mm)
comp_height     = 20.0;    // Max component clearance above PCB (mm)
corner_radius   = 4.0;     // Outer rounded corner radius (mm)

// [Calculated Dimensions - Square Form Factor]
inner_w = pcb_width + 2 * pcb_clearance;                  // 102.0 mm
inner_d = (pcb_depth + 2 * pcb_clearance) + divider_thick + bat_bay_depth; // 82 + 2 + 22 = 106.0 mm
outer_w = inner_w + 2 * wall;                             // 106.8 mm
outer_d = inner_d + 2 * wall;                             // 110.8 mm (Nearly 1:1 Square!)

base_h  = floor_thick + standoff_height + pcb_thickness + 4.0; // 13.0 mm
lid_h   = comp_height - 4.0 + lid_thick;                  // 18.4 mm
total_h = base_h + lid_h;                                 // 31.4 mm (Sleek low-profile)

// =================================================================
// [Sensor Port Coordinates — Relative to PCB bottom-left corner]
// Origin: PCB bottom-left corner
// =================================================================

// 1. AM312 PIR Fresnel Dome Aperture (Flipped into open space)
pir_x = 84.0;
pir_y = 69.2;
pir_dia = 12.0;   // 10mm dome + 2mm clearance

// 2. C1001 60GHz Radar RF Window
radar_x = 90.0;
radar_y = 15.0;
radar_w = 26.0;
radar_d = 26.0;

// 3. LM393 Sound Sensor Acoustic Port (Microphone Hole)
mic_x = 65.5;
mic_y = 53.2;
mic_dia = 3.0;

// 4. Status Fall Alarm LED Hole (3mm LED)
led_x = 90.2;
led_y = 41.0;
led_dia = 3.2;

// 5. Sync Tactile Button Access Pinhole
btn_x = 57.25;
btn_y = 8.75;
btn_dia = 3.5;

// 6. TP4056 USB-C Charging Port Slot (Bottom wall)
usb_x = 26.0;
usb_w = 11.0;
usb_h = 4.8;

// 7. SW2 Power Switch Slot (Left wall)
sw_y = 15.5;
sw_w = 9.5;
sw_h = 5.0;

// [Wall Mount Keyholes]
keyhole_spacing = 60.0;
kh_large_dia = 8.5;
kh_small_dia = 4.5;

// [Ventilation]
vent_slot_w = 1.5;
vent_slot_h = 7.0;
vent_slot_spacing = 5.0;
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
    // Coordinate offsets in centered space:
    // Inner bounds: X in [-inner_w/2, inner_w/2], Y in [-inner_d/2, inner_d/2]
    pcb_ox = -inner_w/2 + pcb_clearance;
    pcb_oy = -inner_d/2 + pcb_clearance;
    div_y = pcb_oy + (pcb_depth + pcb_clearance) + divider_thick/2;

    difference() {
        // Outer Shell
        rounded_box(outer_w, outer_d, base_h, corner_radius);

        // Inner Cavity
        translate([0, 0, floor_thick])
            rounded_box(inner_w, inner_d, base_h, corner_radius - 1);

        // Rear Wall-Mount Keyholes in bottom floor (Spaced 60mm along Y)
        translate([0, -keyhole_spacing/2, -0.5]) keyhole();
        translate([0,  keyhole_spacing/2 - 10, -0.5]) keyhole();

        // USB-C Cutout on bottom wall (Y = -outer_d/2)
        translate([pcb_ox + usb_x, -outer_d/2, floor_thick + standoff_height + pcb_thickness])
            cube([usb_w, wall*2 + 2, usb_h], center=true);

        // Power Switch Cutout on left wall (X = -outer_w/2)
        translate([-outer_w/2, pcb_oy + sw_y, floor_thick + standoff_height + pcb_thickness + 1.0])
            cube([wall*2 + 2, sw_w, sw_h], center=true);

        // Ventilation Slots — Right wall (X = +outer_w/2)
        translate([outer_w/2, -10.0, floor_thick + base_h/2])
            vent_slots(vent_num_slots, vent_slot_w, vent_slot_h, wall);
            
        // Ventilation Slots — Left wall (X = -outer_w/2)
        translate([-outer_w/2, 15.0, floor_thick + base_h/2])
            vent_slots(4, vent_slot_w, vent_slot_h, wall);
    }

    // Divider Wall between PCB and 18650 Battery Bay (with wire pass-through notch)
    translate([0, div_y, floor_thick]) {
        difference() {
            translate([-inner_w/2, -divider_thick/2, 0])
                cube([inner_w, divider_thick, divider_height]);
            // Wire pass-through notch on the left (near BT1)
            translate([-inner_w/2 + 10, -divider_thick, divider_height - 6.0])
                cube([wire_notch_w, divider_thick * 2 + 1, 8.0]);
        }
    }

    // 4 PCB Standoffs (inside the PCB compartment)
    for (sx = [pcb_ox + 4.0, pcb_ox + pcb_width - 4.0]) {
        for (sy = [pcb_oy + 4.0, pcb_oy + pcb_depth - 4.0]) {
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
    pcb_ox = -inner_w/2 + pcb_clearance;
    pcb_oy = -inner_d/2 + pcb_clearance;

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
        // 1. AM312 PIR Fresnel Dome Aperture
        translate([pcb_ox + pir_x, pcb_oy + pir_y, lid_h - lid_thick - 1])
            cylinder(d=pir_dia, h=lid_thick + 3);

        // 2. C1001 Radar RF Window (Thin-wall transmission zone, 1.0mm thick)
        translate([pcb_ox + radar_x - radar_w/2, pcb_oy + radar_y - radar_d/2, lid_h - lid_thick + 1.0])
            cube([radar_w, radar_d, lid_thick]);

        // 3. Microphone Acoustic Inlet Port
        translate([pcb_ox + mic_x, pcb_oy + mic_y, lid_h - lid_thick - 1])
            cylinder(d=mic_dia, h=lid_thick + 3);

        // 4. Status Fall Alarm LED Hole
        translate([pcb_ox + led_x, pcb_oy + led_y, lid_h - lid_thick - 1])
            cylinder(d=led_dia, h=lid_thick + 3);

        // 5. Sync Tactile Button Access Pinhole
        translate([pcb_ox + btn_x, pcb_oy + btn_y, lid_h - lid_thick - 1])
            cylinder(d=btn_dia, h=lid_thick + 3);

        // Ventilation Slots on Lid Side Walls
        translate([outer_w/2, -10.0, lid_h/2])
            vent_slots(vent_num_slots, vent_slot_w, vent_slot_h, wall);

        translate([-outer_w/2, 15.0, lid_h/2])
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
