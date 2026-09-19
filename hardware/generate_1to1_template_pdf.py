import pcbnew
import pymupdf as fitz
import math

MM_TO_PT = 72.0 / 25.4
def mm2pt(mm):
    return mm * MM_TO_PT

board_path = r"C:\Users\devja\Documents\AntiGravity\FallSensorSystem\hardware\fall_sensor.kicad_pcb"
board = pcbnew.LoadBoard(board_path)

doc = fitz.open()

def draw_calibration_ruler(page, x_start_mm, y_start_mm, length_mm=100.0, label="100.0 mm Calibration Ruler (Verify with physical ruler to guarantee true 1:1 scale)"):
    x0 = mm2pt(x_start_mm)
    y0 = mm2pt(y_start_mm)
    w = mm2pt(length_mm)
    h = mm2pt(3.2)
    
    page.draw_rect(fitz.Rect(x0, y0, x0 + w, y0 + h), color=(0.2, 0.2, 0.2), width=0.7)
    for i in range(int(length_mm) + 1):
        tx = x0 + mm2pt(i)
        if i % 10 == 0:
            th = mm2pt(3.2)
            page.draw_line(fitz.Point(tx, y0), fitz.Point(tx, y0 + th), color=(0, 0, 0), width=0.7)
            page.insert_text(fitz.Point(tx - 3, y0 + th + 6.5), f"{i}", fontsize=5.0, fontname="helv", color=(0, 0, 0))
        elif i % 5 == 0:
            th = mm2pt(2.0)
            page.draw_line(fitz.Point(tx, y0), fitz.Point(tx, y0 + th), color=(0.3, 0.3, 0.3), width=0.5)
        else:
            th = mm2pt(1.2)
            page.draw_line(fitz.Point(tx, y0), fitz.Point(tx, y0 + th), color=(0.5, 0.5, 0.5), width=0.3)
            
    page.insert_text(fitz.Point(x0, y0 - 3.5), label, fontsize=7.0, fontname="helv", color=(0, 0, 0))

def draw_crosshair(page, pt, r_mm=3.0, color=(0.8, 0, 0)):
    r = mm2pt(r_mm)
    page.draw_line(fitz.Point(pt.x - r, pt.y), fitz.Point(pt.x + r, pt.y), color=color, width=0.5)
    page.draw_line(fitz.Point(pt.x, pt.y - r), fitz.Point(pt.x, pt.y + r), color=color, width=0.5)


# =========================================================================
# SHEET 1 (PAGE 1): CARRIER PCB - TOP SIDE & BOTTOM SIDE
# =========================================================================
p1 = doc.new_page(width=mm2pt(210.0), height=mm2pt(297.0))

p1.insert_text(fitz.Point(mm2pt(15), mm2pt(8)), "FALL SENSOR - 1:1 TRUE-SCALE CARRIER PCB TEMPLATE (TOP & BOTTOM)", fontsize=10.5, fontname="helv", color=(0, 0, 0))
draw_calibration_ruler(p1, 55.0, 14.0, 100.0)

# -------------------------------------------------------------------------
# TOP PCB: origin at paper X=55mm, Y=34mm (Height 80mm -> Y in [34, 114]mm)
# Board is [50..150, 50..130]. All components inside boundary!
# -------------------------------------------------------------------------
top_ox = 55.0
top_oy = 34.0
def k2top(kx, ky):
    return mm2pt(top_ox + (kx - 50.0)), mm2pt(top_oy + (ky - 50.0))

p1.insert_text(fitz.Point(mm2pt(top_ox), mm2pt(top_oy - 7.0)), "CARRIER PCB: TOP SIDE (Component Placement & Through-Holes)", fontsize=7.5, fontname="helv", color=(0.1, 0.5, 0.2))

# PCB Outline: (50,50) -> (150,50) -> (150,130) -> (60,130) -> (50,120) -> (50,50)
top_poly = [
    fitz.Point(*k2top(50.0, 50.0)),
    fitz.Point(*k2top(150.0, 50.0)),
    fitz.Point(*k2top(150.0, 130.0)),
    fitz.Point(*k2top(60.0, 130.0)),
    fitz.Point(*k2top(50.0, 120.0)),
]
p1.draw_polyline(top_poly + [top_poly[0]], color=(0.1, 0.5, 0.2), fill=(0.96, 0.98, 0.96), width=1.1)

# Chamfer callout
cx1, cy1 = k2top(50.0, 120.0)
cx2, cy2 = k2top(60.0, 130.0)
p1.insert_text(fitz.Point(cx1 - mm2pt(24), cy1 + mm2pt(7)), "10x10mm 45° Chamfer", fontsize=6, fontname="helv", color=(0.7, 0.1, 0.1))
p1.draw_line(fitz.Point(cx1 - mm2pt(2), cy1 + mm2pt(5)), fitz.Point((cx1+cx2)/2, (cy1+cy2)/2), color=(0.8, 0.1, 0.1), width=0.5)

# Dimension lines
p1.draw_line(fitz.Point(*k2top(50.0, 48.0)), fitz.Point(*k2top(150.0, 48.0)), color=(0, 0, 0), width=0.5)
p1.insert_text(fitz.Point(*k2top(95.0, 46.5)), "100.0 mm", fontsize=6.5, fontname="helv", color=(0, 0, 0))
p1.draw_line(fitz.Point(*k2top(152.0, 50.0)), fitz.Point(*k2top(152.0, 130.0)), color=(0, 0, 0), width=0.5)
p1.insert_text(fitz.Point(*k2top(154.0, 92.0)), "80.0 mm", fontsize=6.5, fontname="helv", color=(0, 0, 0))

# Component boxes - accurately positioned inside PCB boundary
top_components = [
    ("U7", "LM2596 Buck Module", (50.53, 50.66, 71.62, 93.84), (0.1, 0.4, 0.7)),
    ("U3", "MT3608 Boost Module", (74.0, 51.0, 110.0, 68.0), (0.1, 0.4, 0.7)),
    ("U4", "TP4056 LiPo Charger", (51.0, 94.5, 78.0, 111.5), (0.1, 0.4, 0.7)),
    ("U2", "Digispark ATtiny85", (67.17, 109.75, 84.67, 128.75), (0.6, 0.2, 0.6)),
    ("U1", "ESP32 DevKit V1 (30-pin)", (90.04, 82.60, 129.36, 113.51), (0.1, 0.3, 0.6)),
    ("RADAR1", "C1001 Radar", (139.5, 110.0, 143.5, 126.5), (0.8, 0.4, 0.1)),
    ("PIR1", "AM312 PIR", (126.5, 49.9, 131.0, 59.4), (0.1, 0.6, 0.3)),
    ("U5", "LM393 Sound", (113.5, 67.5, 117.5, 78.5), (0.7, 0.5, 0.1)),
    ("SW1", "SYNC", (105.0, 119.0, 115.0, 127.5), (0.8, 0.1, 0.1)),
    ("SW2", "SW2", (51.0, 113.0, 54.0, 118.5), (0.8, 0.1, 0.1)),
    ("C1", "C1", (82.0, 86.5, 85.0, 94.5), (0.4, 0.4, 0.4)),
    ("C3", "C3", (87.0, 70.5, 91.0, 77.0), (0.4, 0.4, 0.4)),
]

for ref, label, (x1, y1, x2, y2), col in top_components:
    px1, py1 = k2top(x1, y1)
    px2, py2 = k2top(x2, y2)
    rect = fitz.Rect(min(px1, px2), min(py1, py2), max(px1, px2), max(py1, py2))
    p1.draw_rect(rect, color=col, width=0.6)
    if ref == "U7":
        p1.insert_text(fitz.Point(rect.x0 + mm2pt(2), rect.y0 + mm2pt(15)), "U7: LM2596 Buck", fontsize=5.5, fontname="helv", color=col)
        p1.insert_text(fitz.Point(rect.x0 + mm2pt(2), rect.y0 + mm2pt(19)), "(5V -> 3.3V Step-Down)", fontsize=4.5, fontname="helv", color=col)
    elif ref == "SW2":
        p1.insert_text(fitz.Point(rect.x0 - mm2pt(9), rect.y0 + 5), "SW2", fontsize=5.5, fontname="helv", color=col)
    elif ref == "RADAR1":
        p1.insert_text(fitz.Point(rect.x1 + mm2pt(2), rect.y0 + 8), "RADAR1 (C1001)", fontsize=5.5, fontname="helv", color=col)
    elif ref == "PIR1":
        p1.insert_text(fitz.Point(rect.x0 - mm2pt(4), rect.y1 + mm2pt(3.5)), "PIR1 (AM312)", fontsize=5.5, fontname="helv", color=col)
    elif ref == "U5":
        p1.insert_text(fitz.Point(rect.x1 + mm2pt(2), rect.y0 + 7), "U5 (Sound)", fontsize=5.5, fontname="helv", color=col)
    elif ref == "SW1":
        p1.insert_text(fitz.Point(rect.x0 - mm2pt(16), rect.y0 + 5), "SW1 (SYNC)", fontsize=5.5, fontname="helv", color=col)
    elif ref == "C1":
        p1.insert_text(fitz.Point(rect.x0 - mm2pt(11), rect.y0 + 5), "C1 (10u)", fontsize=5, fontname="helv", color=col)
    elif ref == "C3":
        p1.insert_text(fitz.Point(rect.x1 + mm2pt(2), rect.y0 + 5), "C3 (470u)", fontsize=5, fontname="helv", color=col)
    else:
        p1.insert_text(fitz.Point(rect.x0 + 2, rect.y0 + 6), f"{ref}: {label}", fontsize=5, fontname="helv", color=col)

# Draw Top pads
for pad in board.GetPads():
    parent = pad.GetParentFootprint()
    ref = parent.GetReference() if parent else ""
    pos = pad.GetPosition()
    kx = pos.x / 1e6
    ky = pos.y / 1e6
    px, py = k2top(kx, ky)
    drill = pad.GetDrillSize().x / 1e6
    size = pad.GetSize().x / 1e6
    pad_pt = fitz.Point(px, py)
    r_pad = mm2pt(size / 2.0)
    r_drill = mm2pt(drill / 2.0) if drill > 0 else 0
    if ref == "BT1":
        p1.draw_circle(pad_pt, r_pad, color=(0.9, 0.1, 0.1), fill=(1, 0.8, 0.8), width=0.8)
        if r_drill > 0:
            p1.draw_circle(pad_pt, r_drill, color=(0, 0, 0), fill=(1, 1, 1), width=0.5)
    else:
        p1.draw_circle(pad_pt, r_pad, color=(0.3, 0.3, 0.3), fill=(0.9, 0.9, 0.7), width=0.5)
        if r_drill > 0:
            p1.draw_circle(pad_pt, r_drill, color=(0, 0, 0), fill=(1, 1, 1), width=0.4)

# Top BT1 Callout (Compact labels in open space between BT1 and C3)
p1.insert_text(fitz.Point(*k2top(72.0, 73.5)), "BT1 (Battery Pads)", fontsize=5.0, fontname="helv", color=(0.8, 0, 0))
p1.insert_text(fitz.Point(*k2top(80.2, 75.8)), "BAT+", fontsize=5.0, fontname="helv", color=(0.8, 0, 0))
p1.insert_text(fitz.Point(*k2top(80.2, 78.5)), "BAT-", fontsize=5.0, fontname="helv", color=(0.8, 0, 0))






# -------------------------------------------------------------------------
# BOTTOM PCB: origin at paper X=55mm, Y=148mm (Height 80mm -> Y in [148, 228]mm)
# -------------------------------------------------------------------------
bot_ox = 55.0
bot_oy = 148.0
def k2bot(kx, ky):
    return mm2pt(bot_ox + (kx - 50.0)), mm2pt(bot_oy + (ky - 50.0))

p1.insert_text(fitz.Point(mm2pt(bot_ox), mm2pt(bot_oy - 7.0)), "CARRIER PCB: BOTTOM SIDE (B.Cu Copper Tracks & Battery Routing)", fontsize=7.5, fontname="helv", color=(0.1, 0.3, 0.6))

bot_poly = [
    fitz.Point(*k2bot(50.0, 50.0)),
    fitz.Point(*k2bot(150.0, 50.0)),
    fitz.Point(*k2bot(150.0, 130.0)),
    fitz.Point(*k2bot(60.0, 130.0)),
    fitz.Point(*k2bot(50.0, 120.0)),
]
p1.draw_polyline(bot_poly + [bot_poly[0]], color=(0.1, 0.3, 0.6), fill=(0.96, 0.97, 1.0), width=1.1)

# Chamfer
bcx1, bcy1 = k2bot(50.0, 120.0)
bcx2, bcy2 = k2bot(60.0, 130.0)
p1.insert_text(fitz.Point(bcx1 - mm2pt(24), bcy1 + mm2pt(7)), "10x10mm 45° Chamfer", fontsize=6, fontname="helv", color=(0.1, 0.3, 0.6))

# Dimensions
p1.draw_line(fitz.Point(*k2bot(50.0, 48.0)), fitz.Point(*k2bot(150.0, 48.0)), color=(0, 0, 0), width=0.5)
p1.insert_text(fitz.Point(*k2bot(95.0, 46.5)), "100.0 mm", fontsize=6.5, fontname="helv", color=(0, 0, 0))
p1.draw_line(fitz.Point(*k2bot(152.0, 50.0)), fitz.Point(*k2bot(152.0, 130.0)), color=(0, 0, 0), width=0.5)
p1.insert_text(fitz.Point(*k2bot(154.0, 92.0)), "80.0 mm", fontsize=6.5, fontname="helv", color=(0, 0, 0))

# Draw B.Cu tracks
b_tracks = [t for t in board.GetTracks() if t.GetLayer() == pcbnew.B_Cu]
for t in b_tracks:
    x1 = t.GetStart().x / 1e6
    y1 = t.GetStart().y / 1e6
    x2 = t.GetEnd().x / 1e6
    y2 = t.GetEnd().y / 1e6
    w = t.GetWidth() / 1e6
    pt1 = fitz.Point(*k2bot(x1, y1))
    pt2 = fitz.Point(*k2bot(x2, y2))
    is_batt = (w >= 0.75) and (x1 < 85 and y1 > 70)
    col = (0.9, 0.1, 0.1) if is_batt else (0.2, 0.4, 0.8)
    p1.draw_line(pt1, pt2, color=col, width=mm2pt(max(w, 0.35)))

# Draw bottom through-hole pads
for pad in board.GetPads():
    parent = pad.GetParentFootprint()
    pos = pad.GetPosition()
    kx = pos.x / 1e6
    ky = pos.y / 1e6
    drill = pad.GetDrillSize().x / 1e6
    size = pad.GetSize().x / 1e6
    if drill > 0:
        px, py = k2bot(kx, ky)
        pad_pt = fitz.Point(px, py)
        p1.draw_circle(pad_pt, mm2pt(size / 2.0), color=(0.2, 0.3, 0.6), fill=(0.85, 0.9, 0.98), width=0.5)
        p1.draw_circle(pad_pt, mm2pt(drill / 2.0), color=(0, 0, 0), fill=(1, 1, 1), width=0.4)

# Bottom battery route callout
p1.insert_text(fitz.Point(*k2bot(52.0, 75.0)), "0.8mm Battery Traces", fontsize=5.5, fontname="helv", color=(0.9, 0.1, 0.1))
p1.insert_text(fitz.Point(*k2bot(52.0, 78.0)), "BT1 -> TP4056 Direct", fontsize=5.0, fontname="helv", color=(0.9, 0.1, 0.1))
p1.insert_text(fitz.Point(*k2bot(52.0, 81.0)), "(Zero Planar Crossings)", fontsize=5.0, fontname="helv", color=(0.9, 0.1, 0.1))
p1.draw_line(fitz.Point(*k2bot(68.0, 77.0)), fitz.Point(*k2bot(73.5, 78.0)), color=(0.9, 0.1, 0.1), width=0.5)

# Instructions at bottom of Sheet 1
p1.insert_textbox(fitz.Rect(mm2pt(15), mm2pt(242), mm2pt(195), mm2pt(275)),
"""PCB PRINTING & VERIFICATION INSTRUCTIONS:
1. Print at 100% / 'Actual Size' (never 'Fit to page'). Verify the 100.0 mm calibration bar above.
2. Cut out the green Top PCB shape along the solid line (including the 10x10 mm 45° bottom-left chamfer).
3. Drop the paper into your 3D-printed enclosure base cavity to confirm fitment and standoff clearance (+1.31mm air gap).
4. Poke component pins directly through the through-hole circles to verify header pitch and mechanical clearance.
5. Holding Top and Bottom cutouts up to a light source verifies 100% pin-for-pin alignment for perfboard wiring.""",
fontsize=7.0, fontname="helv", color=(0.2, 0.2, 0.2))


# =========================================================================
# SHEET 2 (PAGE 2): ENCLOSURE BASE & ENCLOSURE LID
# =========================================================================
p2 = doc.new_page(width=mm2pt(210.0), height=mm2pt(297.0))

p2.insert_text(fitz.Point(mm2pt(15), mm2pt(8)), "FALL SENSOR - 1:1 ENCLOSURE BASE & LID TEMPLATE", fontsize=10.5, fontname="helv", color=(0, 0, 0))
draw_calibration_ruler(p2, 55.0, 14.0, 100.0)

# Common enclosure geometry
hw = 116.8 / 2.0
hd = 110.8 / 2.0
ihw = 112.0 / 2.0
ihd = 106.0 / 2.0
boss_x = 53.4
boss_y = 50.4

# -------------------------------------------------------------------------
# TOP: ENCLOSURE BASE (center at X=105, Y=83.4mm -> box from 28.0 to 138.8mm)
# -------------------------------------------------------------------------
base_cx = 105.0
base_cy = 83.4
def b2pt(ex, ey):
    return mm2pt(base_cx + ex), mm2pt(base_cy - ey)

rect_base_outer = fitz.Rect(mm2pt(base_cx - hw), mm2pt(base_cy - hd), mm2pt(base_cx + hw), mm2pt(base_cy + hd))
p2.draw_rect(rect_base_outer, color=(0, 0, 0), fill=(0.98, 0.98, 0.98), width=1.0)
p2.insert_text(fitz.Point(rect_base_outer.x0 + mm2pt(3), rect_base_outer.y0 - mm2pt(2)), "ENCLOSURE BASE: 116.8 x 110.8 x 21.5 mm (Internal Depth: 19.1 mm - Cradles 18650 Battery & PCB)", fontsize=7.5, fontname="helv", color=(0, 0, 0))

rect_base_inner = fitz.Rect(mm2pt(base_cx - ihw), mm2pt(base_cy - ihd), mm2pt(base_cx + ihw), mm2pt(base_cy + ihd))
p2.draw_rect(rect_base_inner, color=(0.5, 0.5, 0.5), fill=(0.94, 0.94, 0.94), width=0.6)

# 4 Corner M3 Bosses
for bx in [-boss_x, boss_x]:
    for by in [-boss_y, boss_y]:
        b_pt = fitz.Point(*b2pt(bx, by))
        p2.draw_circle(b_pt, mm2pt(3.5), color=(0.2, 0.2, 0.6), fill=(0.85, 0.85, 0.95), width=0.7)
        p2.draw_circle(b_pt, mm2pt(1.4), color=(0.1, 0.1, 0.4), fill=(1, 1, 1), width=0.5)

# Battery Cradle: X in [-42.0, 32.0], Y in [30.0, 52.0]
bb_x1, bb_y1 = b2pt(-42.0, 52.0)
bb_x2, bb_y2 = b2pt(32.0, 30.0)
p2.draw_rect(fitz.Rect(bb_x1, bb_y1, bb_x2, bb_y2), color=(0.8, 0.4, 0.1), fill=(1.0, 0.92, 0.85), width=0.8)
p2.insert_text(fitz.Point(bb_x1 + 4, bb_y1 + 10), "18650 Battery Cradle (74.0 x 22.0 mm, Shifted X: -42 to +32)", fontsize=6.0, fontname="helv", color=(0.8, 0.4, 0.1))

# U7 Support Shelf (8x8mm, centered at eX=-44, eY=+24, clear of Pad 2)
sh_x1, sh_y1 = b2pt(-48.0, 28.0)
sh_x2, sh_y2 = b2pt(-40.0, 20.0)
p2.draw_rect(fitz.Rect(sh_x1, sh_y1, sh_x2, sh_y2), color=(0.1, 0.5, 0.2), fill=(0.8, 0.95, 0.8), width=0.8)
p2.insert_text(fitz.Point(sh_x1 + 1, sh_y1 + 7), "U7 Shelf (8x8mm)", fontsize=5.0, fontname="helv", color=(0.1, 0.5, 0.2))
p2.insert_text(fitz.Point(sh_x1 + 1, sh_y1 + 13), "(Clear of Pad 2)", fontsize=4.5, fontname="helv", color=(0.1, 0.5, 0.2))

# 4 Perimeter PCB Support Ledges (4x4mm each, Z=5.0mm, all certified pin/via-free)
ledges_base = [
    ("L1", -53.5, -25.0),  # Safe between U7 Pad 4 and SW2
    ("L2", 43.5, -21.0),   # Open zone between D1 LED and RADAR1
    ("L3", 23.0, -50.5),   # Open zone between SW1 and RADAR1
    ("L4", 19.0, 26.5),    # Open zone between C8 and PIR1
]
for lid, lx, ly in ledges_base:
    lp1 = b2pt(lx - 2.0, ly + 2.0)
    lp2 = b2pt(lx + 2.0, ly - 2.0)
    p2.draw_rect(fitz.Rect(lp1[0], lp1[1], lp2[0], lp2[1]), color=(0.1, 0.5, 0.2), fill=(0.85, 0.96, 0.85), width=0.7)
    if lid == "L1":
        p2.insert_text(fitz.Point(lp1[0] - mm2pt(20), lp1[1] + 5), "Ledge 1 (4x4)", fontsize=4.8, fontname="helv", color=(0.1, 0.5, 0.2))
    elif lid == "L2":
        p2.insert_text(fitz.Point(lp2[0] + 2, lp1[1] + 5), "Ledge 2", fontsize=4.8, fontname="helv", color=(0.1, 0.5, 0.2))
    elif lid == "L3":
        p2.insert_text(fitz.Point(lp1[0] - 2, lp2[1] + 7), "Ledge 3", fontsize=4.8, fontname="helv", color=(0.1, 0.5, 0.2))
    elif lid == "L4":
        p2.insert_text(fitz.Point(lp2[0] + 2, lp1[1] + 5), "Ledge 4", fontsize=4.8, fontname="helv", color=(0.1, 0.5, 0.2))

# Wire notch
wn_x1, wn_y1 = b2pt(-31.0, 31.0)
wn_x2, wn_y2 = b2pt(-23.0, 29.0)
p2.draw_rect(fitz.Rect(wn_x1, wn_y1, wn_x2, wn_y2), color=(0.9, 0.1, 0.1), fill=(1, 1, 1), width=0.8)
p2.insert_text(fitz.Point(wn_x1 - 2, wn_y2 + 7), "Wire Notch (BT1)", fontsize=5.5, fontname="helv", color=(0.9, 0.1, 0.1))

# Centered Wall Hooks (X = 0.0, Y = +/- 25.0)
for ky in [-25.0, 25.0]:
    kh_pt = fitz.Point(*b2pt(0.0, ky))
    p2.draw_circle(kh_pt, mm2pt(4.25), color=(0.4, 0.1, 0.5), width=0.6)
    p2.draw_rect(fitz.Rect(kh_pt.x - mm2pt(2.25), kh_pt.y - mm2pt(4.0), kh_pt.x + mm2pt(2.25), kh_pt.y + mm2pt(4.0)), color=(0.4, 0.1, 0.5), width=0.6)
p2.insert_text(fitz.Point(*b2pt(6.0, 23.0)), "Centered Wall Hook (X = 0.0, Y = +25.0)", fontsize=5.5, fontname="helv", color=(0.4, 0.1, 0.5))
p2.insert_text(fitz.Point(*b2pt(6.0, -25.0)), "Centered Wall Hook (X = 0.0, Y = -25.0)", fontsize=5.5, fontname="helv", color=(0.4, 0.1, 0.5))

# PCB Seated Area
pcb_over_pts = [
    fitz.Point(*b2pt(-55.0, 28.0)),
    fitz.Point(*b2pt(45.0, 28.0)),
    fitz.Point(*b2pt(45.0, -52.0)),
    fitz.Point(*b2pt(-45.0, -52.0)),
    fitz.Point(*b2pt(-55.0, -42.0)),
]
p2.draw_polyline(pcb_over_pts + [pcb_over_pts[0]], color=(0.1, 0.6, 0.2), width=0.9)
p2.insert_text(fitz.Point(*b2pt(-35.0, -10.0)), "PCB Seated Area (100.0 x 80.0 mm) - 1.0 mm Uniform Gap", fontsize=6.0, fontname="helv", color=(0.1, 0.6, 0.2))
p2.insert_text(fitz.Point(*b2pt(-54.0, -36.0)), "+1.31mm Air Gap", fontsize=5.5, fontname="helv", color=(0.7, 0.1, 0.1))

# -------------------------------------------------------------------------
# BOTTOM: ENCLOSURE LID (center at X=105, Y=202.4mm -> box from 147.0 to 257.8mm)
# -------------------------------------------------------------------------
lid_cx = 105.0
lid_cy = 202.4
def l2pt(ex, ey):
    return mm2pt(lid_cx + ex), mm2pt(lid_cy - ey)

rect_lid_outer = fitz.Rect(mm2pt(lid_cx - hw), mm2pt(lid_cy - hd), mm2pt(lid_cx + hw), mm2pt(lid_cy + hd))
p2.draw_rect(rect_lid_outer, color=(0, 0, 0), fill=(1, 1, 1), width=1.0)
p2.insert_text(fitz.Point(rect_lid_outer.x0 + mm2pt(3), rect_lid_outer.y0 - mm2pt(2)), "ENCLOSURE LID: 116.8 x 110.8 x 6.5 mm (Total Height: 28.0 mm - Flared Apertures & Drill Guide)", fontsize=7.5, fontname="helv", color=(0, 0, 0))

# 4 Corner Screw Holes
for bx in [-boss_x, boss_x]:
    for by in [-boss_y, boss_y]:
        pt = fitz.Point(*l2pt(bx, by))
        p2.draw_circle(pt, mm2pt(1.65), color=(0, 0, 0), fill=(0.92, 0.92, 0.92), width=0.8)
        p2.draw_circle(pt, mm2pt(3.2), color=(0.5, 0.5, 0.5), width=0.5)
        draw_crosshair(p2, pt, 3.0, (0.4, 0.4, 0.4))

# Collinear Sensor Axis (X = +37.50 mm)
axis_x, _ = l2pt(37.50, 0)
p2.draw_line(fitz.Point(axis_x, rect_lid_outer.y0 + mm2pt(4)), fitz.Point(axis_x, rect_lid_outer.y1 - mm2pt(4)), color=(0.9, 0.1, 0.1), width=0.6)
p2.insert_text(fitz.Point(axis_x - mm2pt(22), rect_lid_outer.y1 + mm2pt(3.5)), "Collinear Sensor Axis (X = +37.50 mm)", fontsize=6.0, fontname="helv", color=(0.9, 0.1, 0.1))

# PIR dome (dia 12.0 mm inner hole + dia 17.0 mm 45-degree optical flare)
pir_pt = fitz.Point(*l2pt(37.50, 23.39))
p2.draw_circle(pir_pt, mm2pt(8.5), color=(0.9, 0.4, 0.4), width=0.6) # Outer 17mm flare ring
p2.draw_circle(pir_pt, mm2pt(6.0), color=(0.9, 0.1, 0.1), fill=(1, 0.88, 0.88), width=0.9)
draw_crosshair(p2, pir_pt, 6.0, (0.9, 0.1, 0.1))
p2.insert_text(fitz.Point(pir_pt.x + mm2pt(10), pir_pt.y - 4), "PIR1 Dome: 12mm Hole + 17mm 45° Flare", fontsize=6.2, fontname="helv", color=(0.9, 0.1, 0.1))
p2.insert_text(fitz.Point(pir_pt.x + mm2pt(10), pir_pt.y + 4), "Center: (+37.50, +23.39) mm | Dome Protrudes ~2.4mm (360° View)", fontsize=4.8, fontname="helv", color=(0.5, 0.5, 0.5))

# Mic acoustic port (dia 4.5 mm inner hole + dia 9.5 mm 45-degree horn flare)
mic_pt = fitz.Point(*l2pt(37.50, 5.00))
p2.draw_circle(mic_pt, mm2pt(4.75), color=(0.9, 0.4, 0.4), width=0.6) # Outer 9.5mm horn flare
p2.draw_circle(mic_pt, mm2pt(2.25), color=(0.9, 0.1, 0.1), fill=(1, 0.88, 0.88), width=0.9)
draw_crosshair(p2, mic_pt, 3.0, (0.9, 0.1, 0.1))
p2.insert_text(fitz.Point(mic_pt.x + mm2pt(7), mic_pt.y - 4), "LM393 Mic: 4.5mm Port + 9.5mm 45° Horn", fontsize=6.2, fontname="helv", color=(0.9, 0.1, 0.1))
p2.insert_text(fitz.Point(mic_pt.x + mm2pt(7), mic_pt.y + 4), "Center: (+37.50, +5.00) mm | Wide Acoustic Funnel", fontsize=4.8, fontname="helv", color=(0.5, 0.5, 0.5))

# Status LED D1 (dia 3.2 mm inner hole + dia 4.8 mm 45-degree diffuser flare)
led_pt = fitz.Point(*l2pt(37.50, -11.00))
p2.draw_circle(led_pt, mm2pt(2.4), color=(0.9, 0.4, 0.4), width=0.6) # Outer 4.8mm diffuser ring
p2.draw_circle(led_pt, mm2pt(1.6), color=(0.9, 0.1, 0.1), fill=(1, 0.88, 0.88), width=0.9)
draw_crosshair(p2, led_pt, 3.0, (0.9, 0.1, 0.1))
p2.insert_text(fitz.Point(led_pt.x + mm2pt(6), led_pt.y - 4), "Status LED D1: 3.2mm + 4.8mm Diffuser", fontsize=6.2, fontname="helv", color=(0.9, 0.1, 0.1))
p2.insert_text(fitz.Point(led_pt.x + mm2pt(6), led_pt.y + 4), "Center: (+37.50, -11.00) mm | Wide-Angle Glow", fontsize=4.8, fontname="helv", color=(0.5, 0.5, 0.5))

# Built-in ESP32 Contact Boss (14x14 mm, H=3.4mm inside ceiling, roof-mount clamp)
eb_p1 = l2pt(2.0 - 7.0, -19.0 + 7.0)
eb_p2 = l2pt(2.0 + 7.0, -19.0 - 7.0)
p2.draw_rect(fitz.Rect(eb_p1[0], eb_p1[1], eb_p2[0], eb_p2[1]), color=(0.1, 0.3, 0.7), fill=(0.90, 0.94, 1.0), width=0.8)
p2.insert_text(fitz.Point(eb_p1[0] - mm2pt(3), eb_p1[1] - mm2pt(2)), "Built-in ESP32 Contact Boss (14x14mm, H=3.4mm)", fontsize=5.2, fontname="helv", color=(0.1, 0.3, 0.7))
p2.insert_text(fitz.Point(eb_p1[0] - mm2pt(3), eb_p2[1] + mm2pt(3)), "Holds ESP32 metal shield for 28.0mm enclosure (~0.5mm gap)", fontsize=4.6, fontname="helv", color=(0.3, 0.4, 0.6))

# SYNC Button pinhole (dia 3.5 mm inner hole + dia 5.0 mm 45-degree funnel chamfer)
btn_pt = fitz.Point(*l2pt(5.50, -45.50))
p2.draw_circle(btn_pt, mm2pt(2.5), color=(0.8, 0.4, 0.2), width=0.6) # Outer 5.0mm chamfer ring
p2.draw_circle(btn_pt, mm2pt(1.75), color=(0.8, 0.3, 0.1), fill=(1, 0.9, 0.8), width=0.9)
draw_crosshair(p2, btn_pt, 3.0, (0.8, 0.3, 0.1))
p2.insert_text(fitz.Point(btn_pt.x + mm2pt(6), btn_pt.y - 4), "SW1 SYNC Button: 3.5mm + 5.0mm Funnel", fontsize=6.2, fontname="helv", color=(0.8, 0.3, 0.1))
p2.insert_text(fitz.Point(btn_pt.x + mm2pt(6), btn_pt.y + 4), "Center: (+5.50, -45.50) mm | Pen/Pin Guide", fontsize=4.8, fontname="helv", color=(0.5, 0.5, 0.5))

# Instructions at bottom of Sheet 2
p2.insert_textbox(fitz.Rect(mm2pt(15), mm2pt(267), mm2pt(195), mm2pt(292)),
"""ENCLOSURE VERIFICATION INSTRUCTIONS:
1. Place 3D-printed Base directly over the top template: confirm 4 M3 screw boss alignment, centered wall hooks (X=0.0), and cradle boundaries.
2. Place 3D-printed Lid directly over the bottom template: confirm 4 corner screw countersinks, red sensor collinearity, and SYNC button hole.
3. For manual hole drilling or post-processing on the lid, center-punch directly through the crosshairs on this sheet.""",
fontsize=7.0, fontname="helv", color=(0.2, 0.2, 0.2))

# Save 2-page PDF
pdf_path = r"C:\Users\devja\Documents\AntiGravity\FallSensorSystem\hardware\fall_sensor_1to1_scale_template.pdf"
doc.save(pdf_path)
print("Regenerated 2-page 1:1 scale PDF successfully at:", pdf_path)
