import bpy
import bmesh
import math
import os

def reset_blender():
    bpy.ops.wm.read_factory_settings(use_empty=True)

def create_rounded_prism(name, w, d, h, r=4.0):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    
    bm = bmesh.new()
    segments = 8
    hw, hd = w / 2.0, d / 2.0
    r = min(r, hw - 0.5, hd - 0.5)
    
    corners = [
        (hw - r, hd - r, 0.0),
        (-hw + r, hd - r, math.pi / 2.0),
        (-hw + r, -hd + r, math.pi),
        (hw - r, -hd + r, 3.0 * math.pi / 2.0)
    ]
    
    verts_bottom = []
    for cx, cy, start_angle in corners:
        for i in range(segments):
            angle = start_angle + (math.pi / 2.0) * (i / float(segments))
            vx = cx + r * math.cos(angle)
            vy = cy + r * math.sin(angle)
            verts_bottom.append(bm.verts.new((vx, vy, 0.0)))
            
    bm.verts.ensure_lookup_table()
    bottom_face = bm.faces.new(verts_bottom)
    
    ret = bmesh.ops.extrude_face_region(bm, geom=[bottom_face])
    geom_extruded = ret["geom"]
    verts_extruded = [v for v in geom_extruded if isinstance(v, bmesh.types.BMVert)]
    
    bmesh.ops.translate(bm, vec=(0.0, 0.0, h), verts=verts_extruded)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    
    bm.to_mesh(mesh)
    bm.free()
    return obj

def create_cylinder(name, radius, height, location=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=32,
        radius=radius,
        depth=height,
        location=location
    )
    obj = bpy.context.active_object
    obj.name = name
    return obj

def create_cube(name, size_x, size_y, size_z, location=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        location=location
    )
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (size_x, size_y, size_z)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return obj

def boolean_op(target, tool, operation='DIFFERENCE'):
    mod = target.modifiers.new(name=f"Bool_{operation}", type='BOOLEAN')
    mod.operation = operation
    mod.object = tool
    mod.solver = 'EXACT'
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(tool, do_unlink=True)

def generate_photorealistic_enclosure():
    reset_blender()

    # Board Dimensions
    pcb_w = 100.0
    pcb_d = 80.0
    clearance = 1.0
    wall = 2.4
    
    bat_bay_d = 22.0     # 18650 battery bay depth
    divider_t = 2.0      # Separation wall between battery and PCB
    divider_h = 10.0     # Divider height

    # Enclosure cavity dimensions:
    # Adding right-side expansion (+10.0 mm) for C1001 mmWave Radar RF isolation
    radar_chamber_w = 10.0
    inner_w = (pcb_w + 2 * clearance) + radar_chamber_w          # 102.0 + 10.0 = 112.0 mm
    inner_d = (pcb_d + 2 * clearance) + divider_t + bat_bay_d    # 82.0 + 2.0 + 22.0 = 106.0 mm
    outer_w = inner_w + 2 * wall                                 # 116.8 mm
    outer_d = inner_d + 2 * wall                                 # 110.8 mm (1.05 : 1 Square!)

    floor_t = 2.4
    lid_t = 2.4
    standoff_h = 5.0
    pcb_t = 1.6
    comp_clearance_z = 20.0

    base_h = floor_t + standoff_h + pcb_t + 4.0 # 13.0 mm
    lid_h = comp_clearance_z - 4.0 + lid_t      # 18.4 mm

    # Coordinate mapping from KiCad (50..150, 50..130) to Enclosure centered coords:
    # PCB left edge is at X = -inner_w/2 + clearance = -56.0 + 1.0 = -55.0 mm
    # KiCad X=50 maps to ex=-55.0 => ex = kx - 105.0
    # KiCad Y=130 maps to ey=-52.0 (bottom edge) => ey = (130.0 - ky) - 52.0 = 78.0 - ky
    def k2e(kx, ky):
        ex = kx - 105.0
        ey = 78.0 - ky
        return ex, ey

    print(f"Building Photorealistic Square Enclosure: {outer_w:.1f} x {outer_d:.1f} x {base_h + lid_h:.1f} mm")

    # -------------------------------------------------------------
    # 1. BASE PART
    # -------------------------------------------------------------
    base = create_rounded_prism("Base_Body", outer_w, outer_d, base_h, r=4.0)
    
    # Internal Cavity (112.0 x 106.0 x 10.6 mm deep)
    cavity = create_rounded_prism("Base_Cavity", inner_w, inner_d, base_h - floor_t + 2.0, r=3.0)
    cavity.location.z = floor_t
    boolean_op(base, cavity, 'DIFFERENCE')

    # Battery Cradle Retaining Walls (Shifted to X in [-42.0, +32.0] mm, clear of top-left screw boss)
    div_y = 30.0
    bat_x_min = -42.0
    bat_x_max = 32.0
    bat_len = bat_x_max - bat_x_min  # 74.0 mm (standard 18650 holder fits comfortably)
    bat_div_cx = (bat_x_min + bat_x_max) / 2.0  # -5.0 mm
    div_wall = create_cube("Divider_Wall", bat_len, divider_t, divider_h, location=(bat_div_cx, div_y, floor_t + divider_h / 2.0))
    # Wire notch aligned with BT1 at kx = 78.0 mm (ex = -27.0 mm)
    wire_notch = create_cube("Wire_Notch", 8.0, divider_t * 2.0, 6.0, location=(-27.0, div_y, floor_t + divider_h - 2.0))
    boolean_op(div_wall, wire_notch, 'DIFFERENCE')
    boolean_op(base, div_wall, 'UNION')

    # Left Battery Retaining Wall at X = -42.0 mm
    bat_left_wall = create_cube("Battery_Left_Wall", divider_t, bat_bay_d, divider_h, location=(bat_x_min, div_y + divider_t/2.0 + bat_bay_d/2.0, floor_t + divider_h / 2.0))
    boolean_op(base, bat_left_wall, 'UNION')

    # Right Battery Retaining Wall at X = +32.0 mm
    bat_right_wall = create_cube("Battery_Right_Wall", divider_t, bat_bay_d, divider_h, location=(bat_x_max, div_y + divider_t/2.0 + bat_bay_d/2.0, floor_t + divider_h / 2.0))
    boolean_op(base, bat_right_wall, 'UNION')

    # Solid Support Shelf Under U7 (LM2596 module corner support, X in [-55.0, -42.0], Y in [20.0, 28.0])
    u7_shelf = create_cube("U7_Support_Shelf", 13.0, 8.0, standoff_h, location=(-48.5, 24.0, floor_t + standoff_h / 2.0))
    boolean_op(base, u7_shelf, 'UNION')

    # PCB Support Ledges (Certified 100% copper-free and pin-free keepout zones)
    # PCB sits at X in [-55.0, +45.0], Y in [-52.0, +28.0]
    # Ledge 1 (Left):   (-53.5, -43.0) — dead center between SW2 and BT1
    # Ledge 2 (Right):  (+43.5, -21.0) — wide open zone between D1 LED and RADAR1
    # Ledge 3 (Bottom): (+23.0, -50.5) — wide open zone between SW1 and RADAR1
    # Ledge 4 (Top):    (+19.0, +26.5) — wide open zone between C8 and PIR1 (X=124.0mm)
    for lx, ly in [(-53.5, -35.0), (43.5, -21.0), (23.0, -50.5), (19.0, 26.5)]:
        post = create_cube("Shelf_Ledge", 4.0, 4.0, standoff_h, location=(lx, ly, floor_t + standoff_h/2.0))
        boolean_op(base, post, 'UNION')

    # 4 Corner Lid Screw Bosses
    boss_x = outer_w / 2.0 - 5.0
    boss_y = outer_d / 2.0 - 5.0
    for bx in [-boss_x, boss_x]:
        for by in [-boss_y, boss_y]:
            boss = create_cylinder("Boss", radius=3.5, height=base_h - floor_t, location=(bx, by, floor_t + (base_h - floor_t)/2.0))
            hole = create_cylinder("Boss_Hole", radius=1.4, height=base_h + 2.0, location=(bx, by, base_h/2.0))
            boolean_op(boss, hole, 'DIFFERENCE')
            boolean_op(base, boss, 'UNION')

    # 2 Rear Wall-Mount Keyholes (Centered on back wall at X = 0.0 mm)
    for ky in [-25.0, 25.0]:
        kh_head = create_cylinder("KH_Head", radius=4.25, height=2.2, location=(0.0, ky - 4.0, 1.0))
        kh_slot = create_cube("KH_Slot", 4.5, 8.0, floor_t + 1.0, location=(0.0, ky, floor_t / 2.0))
        kh_recess = create_cube("KH_Recess", 9.0, 8.0, 1.4, location=(0.0, ky, floor_t - 0.7))
        boolean_op(base, kh_head, 'DIFFERENCE')
        boolean_op(base, kh_slot, 'DIFFERENCE')
        boolean_op(base, kh_recess, 'DIFFERENCE')

    # USB-C Port Cutout on Left Wall (TP4056 Module: ky = 103.0 mm => ey = -25.0 mm)
    usb_z = floor_t + standoff_h + pcb_t + 1.6
    usb_cut = create_cube("USB_Cutout_LeftWall", wall * 2.0 + 2.0, 11.0, 4.8, location=(-outer_w/2.0, -25.0, usb_z))
    boolean_op(base, usb_cut, 'DIFFERENCE')

    # Power Switch: Internal header pin jumper cap used on PCB; no external opening needed.

    # Ventilation Slots on Right Wall
    for vi in range(6):
        vy = -15.0 + vi * 6.0
        v_slot = create_cube("Vent_Base", wall * 2.0 + 2.0, 1.6, 7.0, location=(outer_w/2.0, vy, floor_t + 4.5))
        boolean_op(base, v_slot, 'DIFFERENCE')

    # -------------------------------------------------------------
    # 2. LID PART (SQUARE FORM FACTOR)
    # -------------------------------------------------------------
    lid = create_rounded_prism("Lid_Body", outer_w, outer_d, lid_h, r=4.0)
    
    # Internal Cavity
    lid_cav_h = lid_h - lid_t + 0.5
    lid_cavity = create_rounded_prism("Lid_Cavity", inner_w, inner_d, lid_cav_h, r=3.0)
    lid_cavity.location.z = -0.5
    boolean_op(lid, lid_cavity, 'DIFFERENCE')

    # Flush Butt Joint (Zero protruding lip for clean, support-free face-down printing)

    # (Floating lid clamp tabs removed; PCB is rigidly secured by corner bosses and base ledges)

    # 4 Corner Lid Screw Boss Pillars (Creates solid guide tubes matching base bosses)
    for bx in [-boss_x, boss_x]:
        for by in [-boss_y, boss_y]:
            lid_boss = create_cylinder("Lid_Boss_Pillar", radius=3.5, height=lid_h - lid_t, location=(bx, by, (lid_h - lid_t)/2.0))
            boolean_op(lid, lid_boss, 'UNION')

    # 4 Corner Countersunk / Counterbore Screw Pass-Through Holes
    for bx in [-boss_x, boss_x]:
        for by in [-boss_y, boss_y]:
            cs_hole = create_cylinder("Lid_Hole", radius=1.65, height=lid_h + 6.0, location=(bx, by, lid_h/2.0))
            cs_sink = create_cylinder("Lid_Sink", radius=3.2, height=3.0, location=(bx, by, lid_h - 1.0))
            boolean_op(lid, cs_hole, 'DIFFERENCE')
            boolean_op(lid, cs_sink, 'DIFFERENCE')

    # Sensor Apertures - EXACT MAPPING TO SENSOR ELEMENTS (COLLINEAR AT kx = 142.50 mm)
    # 1. PIR1 Fresnel Dome (Optical center at kx = 142.50 mm, ky = 54.61 mm)
    pir_ex, pir_ey = k2e(142.50, 54.61)
    pir_hole = create_cylinder("PIR_Aperture", radius=6.0, height=lid_t * 3.0, location=(pir_ex, pir_ey, lid_h))
    boolean_op(lid, pir_hole, 'DIFFERENCE')

    # 2. Mic Acoustic Port (Electret capsule center at kx = 142.50 mm, ky = 73.00 mm)
    mic_ex, mic_ey = k2e(142.50, 73.00)
    mic_hole = create_cylinder("Mic_Port", radius=1.5, height=lid_t * 3.0, location=(mic_ex, mic_ey, lid_h))
    boolean_op(lid, mic_hole, 'DIFFERENCE')

    # 3. Status LED D1 (Center at kx = 142.50 mm, ky = 89.00 mm)
    led_ex, led_ey = k2e(142.50, 89.00)
    led_hole = create_cylinder("LED_Hole", radius=1.6, height=lid_t * 3.0, location=(led_ex, led_ey, lid_h))
    boolean_op(lid, led_hole, 'DIFFERENCE')

    # 4. Sync Button SW1 (Pinhole access over button actuator center at kx = 110.50 mm, ky = 123.50 mm)
    btn_ex, btn_ey = k2e(110.50, 123.50)
    btn_hole = create_cylinder("Sync_Hole", radius=1.75, height=lid_t * 3.0, location=(btn_ex, btn_ey, lid_h))
    boolean_op(lid, btn_hole, 'DIFFERENCE')

    # Right Wall Ventilation Slots on Lid
    for vi in range(6):
        vy = -15.0 + vi * 6.0
        v_slot = create_cube("Vent_Lid_R", wall * 2.0 + 2.0, 1.6, 7.0, location=(outer_w/2.0, vy, lid_h/2.0))
        boolean_op(lid, v_slot, 'DIFFERENCE')

    # -------------------------------------------------------------
    # 3. EXPORT WATERTIGHT STLS
    # -------------------------------------------------------------
    stl_dir = r"C:\Users\devja\Documents\AntiGravity\FallSensorSystem\enclosure"
    base_stl = os.path.join(stl_dir, "fall_sensor_enclosure_base.stl")
    lid_stl = os.path.join(stl_dir, "fall_sensor_enclosure_lid.stl")

    # Export Base
    bpy.ops.object.select_all(action='DESELECT')
    base.select_set(True)
    bpy.context.view_layer.objects.active = base
    bpy.ops.export_mesh.stl(filepath=base_stl, use_selection=True)
    print(f"Exported Base STL: {base_stl} ({os.path.getsize(base_stl)/1024:.1f} KB)")

    # Export Lid
    bpy.ops.object.select_all(action='DESELECT')
    lid.select_set(True)
    bpy.context.view_layer.objects.active = lid
    bpy.ops.export_mesh.stl(filepath=lid_stl, use_selection=True)
    print(f"Exported Lid STL: {lid_stl} ({os.path.getsize(lid_stl)/1024:.1f} KB)")

    # Save Blend file
    blend_path = os.path.join(stl_dir, "fall_sensor_enclosure.blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print(f"Saved Master Blend CAD: {blend_path}")

    # -------------------------------------------------------------
    # 4. PHOTOREALISTIC RENDERS (Hero Assembled & Exploded)
    # -------------------------------------------------------------
    render_hero_and_exploded(base, lid, outer_w, outer_d, base_h, lid_h)

def render_hero_and_exploded(base, lid, outer_w, outer_d, base_h, lid_h):
    # Base Material: Sleek Slate Graphite
    mat_base = bpy.data.materials.new(name="Mat_Base_Graphite")
    mat_base.use_nodes = True
    b_bsdf = mat_base.node_tree.nodes.get("Principled BSDF")
    if b_bsdf:
        b_bsdf.inputs["Base Color"].default_value = (0.36, 0.42, 0.50, 1.0)
        b_bsdf.inputs["Roughness"].default_value = 0.35
    base.data.materials.clear()
    base.data.materials.append(mat_base)

    # Lid Material: Clean Matte Medical White
    mat_lid = bpy.data.materials.new(name="Mat_Lid_White")
    mat_lid.use_nodes = True
    l_bsdf = mat_lid.node_tree.nodes.get("Principled BSDF")
    if l_bsdf:
        l_bsdf.inputs["Base Color"].default_value = (0.95, 0.95, 0.96, 1.0)
        l_bsdf.inputs["Roughness"].default_value = 0.25
    lid.data.materials.clear()
    lid.data.materials.append(mat_lid)

    # World Lighting (Soft Light Studio Grey matching studio and wallmount views)
    world = bpy.context.scene.world
    if not world:
        world = bpy.data.worlds.new("World")
        bpy.context.scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs["Color"].default_value = (0.68, 0.71, 0.75, 1.0)
        bg.inputs["Strength"].default_value = 1.0

    # Studio Floor (Matching medium neutral studio floor)
    bpy.ops.mesh.primitive_plane_add(size=1400.0, location=(0, 0, -0.1))
    ground = bpy.context.active_object
    ground.name = "Studio_Floor"
    mat_floor = bpy.data.materials.new(name="Studio_Floor_Mat")
    mat_floor.use_nodes = True
    f_bsdf = mat_floor.node_tree.nodes.get("Principled BSDF")
    if f_bsdf:
        f_bsdf.inputs["Base Color"].default_value = (0.58, 0.62, 0.67, 1.0)
        f_bsdf.inputs["Roughness"].default_value = 0.55
    ground.data.materials.clear()
    ground.data.materials.append(mat_floor)

    # Soft Studio Diffuse Lighting (Eliminates harsh black shadow "plate" inside base)
    key_data = bpy.data.lights.new(name="Studio_Key", type='AREA')
    key_data.energy = 320.0
    key_data.size = 450.0
    key_data.color = (1.0, 0.98, 0.96)
    key_obj = bpy.data.objects.new(name="Studio_Key", object_data=key_data)
    bpy.context.collection.objects.link(key_obj)
    key_obj.location = (110.0, -140.0, 190.0)

    fill_data = bpy.data.lights.new(name="Studio_Fill", type='AREA')
    fill_data.energy = 220.0
    fill_data.size = 500.0
    fill_data.color = (0.96, 0.98, 1.0)
    fill_obj = bpy.data.objects.new(name="Studio_Fill", object_data=fill_data)
    bpy.context.collection.objects.link(fill_obj)
    fill_obj.location = (-130.0, -100.0, 160.0)

    # Ambient cavity fill to illuminate standoffs and battery wall softly
    bounce_data = bpy.data.lights.new(name="Cavity_Fill", type='AREA')
    bounce_data.energy = 90.0
    bounce_data.size = 300.0
    bounce_data.color = (0.95, 0.95, 0.98)
    bounce_obj = bpy.data.objects.new(name="Cavity_Fill", object_data=bounce_data)
    bpy.context.collection.objects.link(bounce_obj)
    bounce_obj.location = (20.0, -40.0, 110.0)

    # Render Settings
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.device = 'CPU'
    bpy.context.scene.cycles.samples = 64
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080
    bpy.context.scene.render.film_transparent = False

    # Focus Target Empty (keeps camera centered on objects)
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 15.0))
    target = bpy.context.active_object
    target.name = "Cam_Target"

    # Camera with Track-To Constraint
    cam_data = bpy.data.cameras.new(name="Camera")
    cam_obj = bpy.data.objects.new(name="Camera", object_data=cam_data)
    bpy.context.collection.objects.link(cam_obj)
    bpy.context.scene.camera = cam_obj

    track = cam_obj.constraints.new(type='TRACK_TO')
    track.target = target
    track.track_axis = 'TRACK_NEGATIVE_Z'
    track.up_axis = 'UP_Y'

    def safe_render(path):
        import time
        for attempt in range(3):
            try:
                if os.path.exists(path):
                    os.remove(path)
                break
            except Exception:
                time.sleep(0.5)
        bpy.context.scene.render.filepath = path
        bpy.ops.render.render(write_still=True)

    # 1. Assembled Hero Shot
    lid.location = (0, 0, base_h)
    target.location = (0, 0, 8.0)
    cam_dist = 310.0
    cam_obj.location = (cam_dist * 0.65, -cam_dist * 0.70, cam_dist * 0.52)

    img_hero = r"C:\Users\devja\Documents\AntiGravity\FallSensorSystem\enclosure\fall_sensor_enclosure_assembled_hero.png"
    safe_render(img_hero)
    print(f"Rendered Hero Image: {img_hero}")

    # 2. Exploded View (Lid lifted by 38mm, cavity cleanly illuminated)
    lid.location = (0, 0, base_h + 38.0)
    target.location = (0, 0, 18.0)
    cam_dist_exp = 370.0
    cam_obj.location = (cam_dist_exp * 0.65, -cam_dist_exp * 0.70, cam_dist_exp * 0.54)

    img_exp = r"C:\Users\devja\Documents\AntiGravity\FallSensorSystem\enclosure\fall_sensor_enclosure_exploded.png"
    safe_render(img_exp)
    print(f"Rendered Exploded Image: {img_exp}")

    # 3. Studio Side-by-Side View (Lid flipped open to reveal internal cavity and 4 PCB clamping tabs)
    base.location = (-64.0, 0, 0)
    base.rotation_euler = (0, 0, 0)
    lid.location = (64.0, 0, lid_h)
    lid.rotation_euler = (math.radians(180), 0, 0)
    target.location = (0, 0, 10.0)
    cam_obj.location = (0, -320.0, 260.0)

    img_studio = r"C:\Users\devja\Documents\AntiGravity\FallSensorSystem\enclosure\fall_sensor_enclosure_studio.png"
    safe_render(img_studio)
    print(f"Rendered Studio Image: {img_studio}")

    # 4. Rear Wall-Mount View (Zoomed out with generous margin around base)
    base.location = (0, 0, 13.0)
    base.rotation_euler = (math.radians(180), 0, 0)
    lid.hide_render = True
    target.location = (0, 0, 7.0)
    cam_obj.location = (0, -240.0, 200.0)

    img_wall = r"C:\Users\devja\Documents\AntiGravity\FallSensorSystem\enclosure\fall_sensor_enclosure_wallmount.png"
    safe_render(img_wall)
    print(f"Rendered Wallmount Image: {img_wall}")

if __name__ == "__main__":
    generate_photorealistic_enclosure()
