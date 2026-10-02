"""Procedural generic phone and the three RuteAman trailer shots.

Run headless from the repo root:
  blender -b -P blender/phone.py -- --shot hook --still 110
  blender -b -P blender/phone.py -- --shot hook --frames 0 204
  blender -b -P blender/phone.py -- --shot hook --align     (writes the b8 handoff table)
Options: --engine eevee|cycles, --samples N, --scale PCT, --out DIR.
Scene frame numbers are film frames (30 fps), so a screen video and a 3D clip share one clock.
"""

import argparse
import json
import math
import os
import sys
import time

import bmesh
import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Matrix, Vector

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MM = 0.001

# Size: the active area keeps the recordings' 1080:2400 aspect (Pixel 7 emulator), so the texture is never stretched.
H = 152 * MM
T = 8 * MM
GLASS_INSET = 0.9 * MM  # frame lip around the front glass
BEZEL = 1.3 * MM  # black border between the glass edge and the active area
AH = H - 2 * (GLASS_INSET + BEZEL)
AW = AH * 1080 / 2400
W = AW + 2 * (GLASS_INSET + BEZEL)
R = 10 * MM  # outline corner radius
ZG = T / 2 + 0.25 * MM  # front glass surface

TEX_W, TEX_H = 1080, 2400


def tex_to_local(px, py):
    return Vector(((px / TEX_W - 0.5) * AW, (0.5 - py / TEX_H) * AH, ZG))


# --------------------------------------------------------------------------- geometry

def rounded_rect(w, h, r, segs=24):
    pts = []
    for cx, cy, a0 in ((w / 2 - r, h / 2 - r, 0), (-w / 2 + r, h / 2 - r, 90), (-w / 2 + r, -h / 2 + r, 180), (w / 2 - r, -h / 2 + r, 270)):
        for i in range(segs + 1):
            a = math.radians(a0 + 90 * i / segs)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def slab(name, outline, z0, z1, mat_cap=None, mat_side=None, mat_bottom=None, bevel=0.0, bevel_segs=5, profile=0.5, uv_fn=None):
    """Extrude a closed 2D outline between z0 and z1. Optional smooth-chamfer bevel on the cap edges."""
    mesh = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bot = [bm.verts.new((x, y, z0)) for x, y in outline]
    top = [bm.verts.new((x, y, z1)) for x, y in outline]
    n = len(outline)
    f_top = bm.faces.new(top)
    f_bot = bm.faces.new(list(reversed(bot)))
    sides = [bm.faces.new((bot[i], bot[(i + 1) % n], top[(i + 1) % n], top[i])) for i in range(n)]
    mats = [m for m in (mat_cap, mat_side, mat_bottom) if m]
    uniq = []
    for m in mats:
        if m not in uniq:
            uniq.append(m)
    for m in uniq:
        mesh.materials.append(m)
    idx = lambda m: uniq.index(m) if m in uniq else 0
    f_top.material_index = idx(mat_cap)
    f_bot.material_index = idx(mat_bottom or mat_side or mat_cap)
    for f in sides:
        f.material_index = idx(mat_side or mat_cap)
    uv = bm.loops.layers.uv.new("UVMap")
    for f in bm.faces:
        for loop in f.loops:
            co = loop.vert.co
            loop[uv].uv = uv_fn(co, f is f_top) if uv_fn else (co.x / W + 0.5, co.y / H + 0.5)
    for f in bm.faces:
        f.smooth = True
    bm.to_mesh(mesh)
    bm.free()
    mesh.set_sharp_from_angle(angle=math.radians(35))
    ob = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(ob)
    if bevel > 0:
        mod = ob.modifiers.new("Chamfer", "BEVEL")
        mod.width = bevel
        mod.segments = bevel_segs
        mod.profile = profile
        mod.limit_method = "ANGLE"
        mod.angle_limit = math.radians(35)
        mod.harden_normals = True
        mod.use_clamp_overlap = True
    wn = ob.modifiers.new("WeightedNormal", "WEIGHTED_NORMAL")
    wn.keep_sharp = True
    return ob


def cylinder(name, r, z0, z1, mat, x=0.0, y=0.0, bevel=0.0, segs=96):
    pts = [(x + r * math.cos(2 * math.pi * i / segs), y + r * math.sin(2 * math.pi * i / segs)) for i in range(segs)]
    return slab(name, pts, z0, z1, mat_cap=mat, bevel=bevel, bevel_segs=4)


def transform_mesh(ob, m):
    ob.data.transform(m)
    ob.data.update()


# --------------------------------------------------------------------------- materials

def principled(name, base, metallic=0.0, rough=0.5, coat=0.0, coat_rough=0.03, ior=1.5, spec=0.5):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*base, 1)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["IOR"].default_value = ior
    bsdf.inputs["Specular IOR Level"].default_value = spec
    bsdf.inputs["Coat Weight"].default_value = coat
    bsdf.inputs["Coat Roughness"].default_value = coat_rough
    return mat


def screen_material(seq_dir, frame_start, frames):
    """Black cover glass with a clear coat; the active area emits the screen video through the planar UVs."""
    mat = principled("ScreenGlass", (0.0, 0.0, 0.0), rough=0.035, coat=1.0, coat_rough=0.015, spec=0.5)
    nt = mat.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    img = bpy.data.images.load(os.path.join(seq_dir, "0001.jpg"), check_existing=True)
    img.source = "SEQUENCE"
    img.colorspace_settings.name = "Non-Color"
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = img
    tex.extension = "CLIP"
    tex.interpolation = "Linear"
    tex.image_user.frame_duration = frames
    tex.image_user.frame_start = frame_start
    tex.image_user.frame_offset = 0
    tex.image_user.use_auto_refresh = True
    uvn = nt.nodes.new("ShaderNodeUVMap")
    uvn.uv_map = "UVMap"
    nt.links.new(uvn.outputs["UV"], tex.inputs["Vector"])
    # Per-channel inverse of the Filmic view transform: sRGB code value -> scene-linear emission that
    # Filmic displays as the same code value, so the UI keeps its colours (mint, amber, SOS red).
    lut = nt.nodes.new("ShaderNodeTexImage")
    lut.image = inverse_lut_image()
    lut.interpolation = "Linear"
    lut.extension = "EXTEND"
    sep = nt.nodes.new("ShaderNodeSeparateColor")
    comb = nt.nodes.new("ShaderNodeCombineColor")
    nt.links.new(tex.outputs["Color"], sep.inputs["Color"])
    for i, ch in enumerate(("Red", "Green", "Blue")):
        mad = nt.nodes.new("ShaderNodeMath")
        mad.operation = "MULTIPLY_ADD"
        mad.inputs[1].default_value = 255 / 256
        mad.inputs[2].default_value = 0.5 / 256
        nt.links.new(sep.outputs[i], mad.inputs[0])
        xyz = nt.nodes.new("ShaderNodeCombineXYZ")
        xyz.inputs["Y"].default_value = 0.5
        nt.links.new(mad.outputs[0], xyz.inputs["X"])
        look = nt.nodes.new("ShaderNodeTexImage")
        look.image = lut.image
        look.interpolation = "Linear"
        look.extension = "EXTEND"
        nt.links.new(xyz.outputs["Vector"], look.inputs["Vector"])
        sep_l = nt.nodes.new("ShaderNodeSeparateColor")
        nt.links.new(look.outputs["Color"], sep_l.inputs["Color"])
        nt.links.new(sep_l.outputs[0], comb.inputs[ch])
    nt.nodes.remove(lut)
    nt.links.new(comb.outputs["Color"], bsdf.inputs["Emission Color"])
    bsdf.inputs["Emission Strength"].default_value = SCREEN_GAIN
    return mat, bsdf


VIEW = "Filmic"
LUT_PATH = os.path.join(ROOT, "blender", "view-inverse.json")
LUT_CAP = 4.0  # scene-linear ceiling for UI white (Filmic shows ~242): bright, but no clipped hot spots


def inverse_lut_image():
    with open(LUT_PATH) as fh:
        need = json.load(fh)["linear"]
    img = bpy.data.images.new("ViewInverse", 256, 1, float_buffer=True)
    img.colorspace_settings.name = "Non-Color"
    px = []
    for v in need:
        v = min(v, LUT_CAP)
        px += [v, v, v, 1.0]
    img.pixels.foreach_set(px)
    return img


def calibrate():
    """Render a log ramp of emission values through the view transform and invert it into a 256-entry LUT."""
    sc = bpy.context.scene
    for ob in list(bpy.data.objects):
        bpy.data.objects.remove(ob)
    n = 2048
    lin = [1e-5 * (64 / 1e-5) ** (i / (n - 1)) for i in range(n)]
    ramp = bpy.data.images.new("ramp", n, 1, float_buffer=True)
    ramp.colorspace_settings.name = "Non-Color"
    px = []
    for v in lin:
        px += [v, v, v, 1.0]
    ramp.pixels.foreach_set(px)
    mesh = bpy.data.meshes.new("plane")
    mesh.from_pydata([(-1, -1, 0), (1, -1, 0), (1, 1, 0), (-1, 1, 0)], [], [(0, 1, 2, 3)])
    uv = mesh.uv_layers.new()
    for loop, co in zip(uv.data, ((0, 0), (1, 0), (1, 1), (0, 1))):
        loop.uv = co
    plane = bpy.data.objects.new("plane", mesh)
    sc.collection.objects.link(plane)
    mat = bpy.data.materials.new("ramp")
    mat.use_nodes = True
    nt = mat.node_tree
    for nd in list(nt.nodes):
        nt.nodes.remove(nd)
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image, tex.interpolation = ramp, "Closest"
    em = nt.nodes.new("ShaderNodeEmission")
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(tex.outputs[0], em.inputs[0])
    nt.links.new(em.outputs[0], out.inputs[0])
    mesh.materials.append(mat)
    cd = bpy.data.cameras.new("cal")
    cd.type, cd.ortho_scale = "ORTHO", 2
    cam = bpy.data.objects.new("cal", cd)
    sc.collection.objects.link(cam)
    cam.location = (0, 0, 2)
    sc.camera = cam
    sc.render.engine = "BLENDER_EEVEE"
    sc.eevee.taa_render_samples = 1
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = n, 4, 100
    sc.render.film_transparent = False
    sc.view_settings.view_transform, sc.view_settings.look = VIEW, "None"
    path = os.path.join(bpy.app.tempdir or "/tmp", "view-ramp.png")
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_depth = "16"
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)
    shown = bpy.data.images.load(path)
    shown.colorspace_settings.name = "Non-Color"
    vals = list(shown.pixels)
    disp = [vals[(2 * n + i) * 4] for i in range(n)]
    need = []
    for code in range(256):
        target = code / 255
        j = next((k for k in range(n) if disp[k] >= target), n - 1)
        if j == 0:
            need.append(0.0)
            continue
        d0, d1 = disp[j - 1], disp[j]
        t = 0 if d1 == d0 else (target - d0) / (d1 - d0)
        need.append(lin[j - 1] + t * (lin[j] - lin[j - 1]))
    need[0] = 0.0
    with open(LUT_PATH, "w") as fh:
        json.dump({"view": VIEW, "look": "None", "linear": [round(v, 6) for v in need]}, fh)
    print("LUT", LUT_PATH, [round(need[c], 4) for c in (10, 30, 60, 120, 180, 230, 255)])


# Emission gain on top of the inverse LUT (1.0 = the screen shows the composition's pixels).
SCREEN_GAIN = 1.0


def build_phone():
    alu = principled("GraphiteAluminium", (0.1, 0.1, 0.108), metallic=1.0, rough=0.32)
    alu_bright = principled("LensRing", (0.12, 0.12, 0.125), metallic=1.0, rough=0.18)
    back = principled("BackGlass", (0.012, 0.012, 0.014), rough=0.48, spec=0.3)
    module_glass = principled("ModuleGlass", (0.012, 0.012, 0.014), rough=0.12, coat=1.0, coat_rough=0.03)
    lens = principled("Lens", (0.0, 0.0, 0.0), rough=0.02, coat=1.0, coat_rough=0.0)
    lens_inner = principled("LensInner", (0.03, 0.032, 0.04), metallic=0.4, rough=0.25)
    flash = principled("Flash", (0.55, 0.53, 0.48), rough=0.45)
    black = principled("BlackGlass", (0.0, 0.0, 0.0), rough=0.05, coat=0.6)

    rig = bpy.data.objects.new("PhoneRig", None)
    bpy.context.scene.collection.objects.link(rig)
    parts = []

    # Frame: satin graphite aluminium with a smooth chamfer on both faces.
    body = slab("Frame", rounded_rect(W, H, R, 32), -T / 2, T / 2, mat_cap=alu, bevel=0.85 * MM, bevel_segs=6, profile=0.62)
    parts.append(body)

    # Front glass: planar UVs over the active area. Everything outside 0..1 samples CLIP black = bezel.
    def screen_uv(co, is_top):
        if not is_top:
            return (-1.0, -1.0)
        return ((co.x + AW / 2) / AW, (co.y + AH / 2) / AH)

    gw, gh, gr = W - 2 * GLASS_INSET, H - 2 * GLASS_INSET, R - GLASS_INSET
    glass = slab("FrontGlass", rounded_rect(gw, gh, gr, 32), T / 2 - 0.6 * MM, ZG, mat_cap=black, bevel=0.32 * MM, bevel_segs=4, profile=0.55, uv_fn=screen_uv)
    parts.append(glass)

    backp = slab("BackGlass", rounded_rect(gw, gh, gr, 32), -ZG, -T / 2 + 0.6 * MM, mat_cap=back, bevel=0.3 * MM, bevel_segs=3)
    parts.append(backp)

    # Side keys on +X (right edge seen from the front): a long volume key and a short power key.
    for name, cy, length in (("VolumeKey", 26 * MM, 21 * MM), ("PowerKey", 3 * MM, 10 * MM)):
        key = slab(name, rounded_rect(length, 2.4 * MM, 1.1 * MM, 12), 0, 0.55 * MM, mat_cap=alu, bevel=0.22 * MM, bevel_segs=3)
        transform_mesh(key, Matrix.Translation((W / 2 - 0.1 * MM, cy, 0)) @ Matrix.Rotation(math.radians(90), 4, "Y") @ Matrix.Rotation(math.radians(90), 4, "Z"))
        parts.append(key)

    # USB-C port on the bottom edge.
    port = slab("Port", rounded_rect(8.4 * MM, 2.6 * MM, 1.3 * MM, 12), 0, 0.05 * MM, mat_cap=principled("Port", (0.004, 0.004, 0.005), rough=0.6))
    transform_mesh(port, Matrix.Translation((0, -H / 2 + 0.02 * MM, 0)) @ Matrix.Rotation(math.radians(90), 4, "X"))
    parts.append(port)

    # Back camera island, top-left seen from the back (+X side). Two lenses and a flash beside it.
    mx, my = W / 2 - 15.5 * MM, H / 2 - 22 * MM
    island = slab("CameraIsland", rounded_rect(20 * MM, 33 * MM, 8 * MM, 24), 0, 1.0 * MM, mat_cap=module_glass, mat_side=alu, bevel=0.35 * MM, bevel_segs=4)
    flip = Matrix.Rotation(math.radians(180), 4, "Y")
    transform_mesh(island, Matrix.Translation((mx, my, -ZG + 0.05 * MM)) @ flip)
    parts.append(island)
    for i, dy in enumerate((7.6 * MM, -7.6 * MM)):
        ring = cylinder(f"LensRing{i}", 6.3 * MM, 0, 0.45 * MM, alu_bright, bevel=0.16 * MM)
        transform_mesh(ring, Matrix.Translation((mx, my + dy, -ZG - 0.95 * MM)) @ flip)
        glass_l = cylinder(f"Lens{i}", 5.2 * MM, 0, 0.55 * MM, lens, bevel=0.08 * MM)
        transform_mesh(glass_l, Matrix.Translation((mx, my + dy, -ZG - 0.95 * MM)) @ flip)
        inner = cylinder(f"LensInner{i}", 2.6 * MM, 0, 0.57 * MM, lens_inner)
        transform_mesh(inner, Matrix.Translation((mx, my + dy, -ZG - 0.95 * MM)) @ flip)
        parts += [ring, glass_l, inner]
    fl = cylinder("Flash", 1.9 * MM, 0, 0.12 * MM, flash, bevel=0.05 * MM)
    transform_mesh(fl, Matrix.Translation((mx - 14.5 * MM, my + 9 * MM, -ZG)) @ flip)
    parts.append(fl)

    for p in parts:
        p.parent = rig
    return rig, glass


# --------------------------------------------------------------------------- scene

def look_at(ob, target):
    """Point local -Z at target with local +Y toward world +Y (the scene is Y-up; to_track_quat assumes Z-up)."""
    fwd = (Vector(target) - Vector(ob.location)).normalized()
    z = -fwd
    x = Vector((0, 1, 0)).cross(z).normalized()
    y = z.cross(x)
    ob.rotation_euler = Matrix((x, y, z)).transposed().to_euler()


def area_light(name, size, size_y, energy, loc, target, spread=180):
    data = bpy.data.lights.new(name, "AREA")
    data.shape = "RECTANGLE"
    data.size, data.size_y = size, size_y
    data.energy = energy
    data.spread = math.radians(spread)
    ob = bpy.data.objects.new(name, data)
    bpy.context.scene.collection.objects.link(ob)
    ob.location = loc
    look_at(ob, target)
    return ob


def setup_scene(engine, samples, scale):
    sc = bpy.context.scene
    for ob in list(bpy.data.objects):
        bpy.data.objects.remove(ob)
    sc.render.resolution_x, sc.render.resolution_y = 1920, 1080
    sc.render.resolution_percentage = scale
    sc.render.fps = 30
    sc.render.film_transparent = True
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGBA"
    sc.render.image_settings.color_depth = "8"
    sc.render.use_motion_blur = True
    sc.render.motion_blur_shutter = 0.5
    sc.view_settings.view_transform = VIEW
    sc.view_settings.look = "None"
    sc.view_settings.exposure = 0.0
    sc.world = bpy.data.worlds.new("Studio")
    sc.world.use_nodes = True
    bg = sc.world.node_tree.nodes["Background"]
    bg.inputs["Color"].default_value = (0, 0, 0, 1)
    bg.inputs["Strength"].default_value = 0.0
    if engine == "eevee":
        sc.render.engine = "BLENDER_EEVEE"
        ee = sc.eevee
        ee.taa_render_samples = samples
        for attr, val in (("use_raytracing", True), ("use_shadows", True), ("motion_blur_steps", 1), ("use_volumetric_shadows", False)):
            if hasattr(ee, attr):
                setattr(ee, attr, val)
        try:
            ee.ray_tracing_options.resolution_scale = "1"
        except (AttributeError, TypeError):
            pass
        if hasattr(ee, "shadow_ray_count"):
            ee.shadow_ray_count = 2
            ee.shadow_step_count = 8
    else:
        sc.render.engine = "CYCLES"
        prefs = bpy.context.preferences.addons["cycles"].preferences
        for backend in ("OPTIX", "CUDA"):
            try:
                prefs.compute_device_type = backend
                prefs.get_devices()
                if any(d.type == backend for d in prefs.devices):
                    break
            except TypeError:
                continue
        for d in prefs.devices:
            d.use = d.type in ("OPTIX", "CUDA")
        sc.cycles.device = "GPU"
        sc.cycles.samples = samples
        sc.cycles.use_adaptive_sampling = True
        sc.cycles.adaptive_threshold = 0.02
        sc.cycles.use_denoising = True
        sc.cycles.denoiser = "OPENIMAGEDENOISE"
        sc.cycles.max_bounces = 6
        sc.cycles.glossy_bounces = 4
        sc.cycles.transmission_bounces = 4
        sc.cycles.caustics_reflective = False
        sc.cycles.caustics_refractive = False
        sc.cycles.film_exposure = 1.0
    return sc


def make_camera(lens=85):
    cam_data = bpy.data.cameras.new("Camera")
    cam_data.lens = lens
    cam_data.sensor_width = 36
    cam_data.sensor_fit = "HORIZONTAL"
    cam_data.clip_start = 0.01
    cam_data.clip_end = 20
    cam_data.dof.use_dof = True
    cam = bpy.data.objects.new("Camera", cam_data)
    bpy.context.scene.collection.objects.link(cam)
    bpy.context.scene.camera = cam
    return cam


# --------------------------------------------------------------------------- animation helpers

def key(ob, path, frame, value):
    setattr(ob, path, value)
    ob.keyframe_insert(data_path=path, frame=frame)


def shape_curves(id_data, ease=0.6):
    """Bezier keys with flat handles. Longer handles (ease -> 1) give a power4.inOut-like move:
    slow start, quick middle, a long settle onto the key."""
    ad = id_data.animation_data
    if not ad or not ad.action:
        return
    curves = []
    action = ad.action
    if hasattr(action, "fcurves") and len(getattr(action, "fcurves", [])):
        curves = list(action.fcurves)
    else:
        for layer in getattr(action, "layers", []):
            for strip in layer.strips:
                for bag in strip.channelbags:
                    curves += list(bag.fcurves)
    for fc in curves:
        kps = fc.keyframe_points
        for i, kp in enumerate(kps):
            kp.interpolation = "BEZIER"
            kp.handle_left_type = kp.handle_right_type = "FREE"
            x, y = kp.co
            prev_dx = (x - kps[i - 1].co.x) if i > 0 else 10
            next_dx = (kps[i + 1].co.x - x) if i < len(kps) - 1 else 10
            kp.handle_left = (x - prev_dx * ease, y)
            kp.handle_right = (x + next_dx * ease, y)


# --------------------------------------------------------------------------- shots

def deg(*a):
    return tuple(math.radians(v) for v in a)


SHOTS = {
    # 0 to 6.83 s. Emerges from darkness at 3/4, turns ~15 deg toward camera, then pushes into the dot.
    "hook": dict(video="screen-a", video_start=0, video_frames=205, frames=(0, 204), still=110, fstop=2.8),
    # 36.33 to 41.67 s. Floats on the right with a gentle tilt, slow 10 deg orbit.
    "protect": dict(video="screen-b", video_start=1090, video_frames=165, frames=(1090, 1252), still=1170, fstop=3.2),
    # 48.0 to 54.17 s. Hero turn from a 3/4 back view to the front, settles at b62 (f1550), then holds.
    "end": dict(video="screen-c", video_start=1430, video_frames=195, frames=(1440, 1552), still=1530, fstop=3.2),
}


def frame_px_per_m(d, lens=85):
    return 1920 * (lens / 1000) / (0.036 * d)


def setup_lights(shot, phone_parts, glass):
    """Studio set: large soft key, thin rims for the frame edges, and one soft strip that is the only
    light the screen glass reflects (light linking), so reflections stay a gentle sweep, never a wash."""
    tgt = (0, 0, 0)
    body = bpy.data.collections.new("LitBody")
    for p in phone_parts:
        if p is not glass:
            body.objects.link(p)
    face = bpy.data.collections.new("LitGlass")
    face.objects.link(glass)
    lights = dict(
        key=area_light("Key", 1.4, 1.0, 28, (-0.9, 1.1, 1.3), tgt),
        rim_r=area_light("RimRight", 0.06, 1.6, 34, (0.95, 0.15, -0.55), tgt),
        rim_l=area_light("RimLeft", 0.06, 1.6, 20, (-0.95, 0.35, -0.5), tgt),
        fill=area_light("Fill", 1.6, 1.6, 6, (0.9, -0.6, 1.2), tgt),
        sweep=area_light("Sweep", 0.2, 1.4, 1.4, (-0.8, 0.1, 0.85), tgt),
    )
    for name, ob in lights.items():
        ob.light_linking.receiver_collection = face if name == "sweep" else body
    if shot == "protect":
        lights["sweep"].location = (-0.95, 0.3, 0.55)
    elif shot == "end":
        # Reflects as the phone passes yaw +13 deg, just before it settles at -14 deg, then leaves the glass clear.
        lights["sweep"].location = (0.42, 0.25, 0.9)
    for ob in lights.values():
        look_at(ob, tgt)
    return lights


def anim_hook(rig, cam, lights, glass_bsdf, focus):
    cam.data.dof.focus_object = focus
    d0 = 1.063
    ppm0 = frame_px_per_m(d0)
    # Phone centre at frame x 1360: the camera axis sits 400 px left of it.
    cam.rotation_euler = (0, 0, 0)
    key(cam, "location", 0, (-400 / ppm0, 0.004, d0))
    key(cam, "location", 164, (-400 / ppm0, 0.0, d0))
    # Handoff at b8: the push lands at f194 and holds. The dot (tex 540,1702) sits on frame (1360,726) at
    # 0.97 frame px per tex px = 1.116 frame px per map px, so the world map in index.html opens at 1.15x
    # with its bottom edge just below the frame.
    dot = tex_to_local(540, 1702)
    ppm1 = 0.97 / (AW / TEX_W)
    d1 = 1920 * 0.085 / (0.036 * ppm1)
    key(cam, "location", 194, (dot.x - 400 / ppm1, dot.y + 186 / ppm1, ZG + d1))
    key(cam, "location", 204, (dot.x - 400 / ppm1, dot.y + 186 / ppm1, ZG + d1))
    # Phone: 3/4 yaw easing toward camera (about 15 deg over the shot), slight pitch, square at the push.
    key(rig, "rotation_euler", 0, deg(6, -28, 2))
    key(rig, "rotation_euler", 164, deg(2, -13, 0.5))
    key(rig, "rotation_euler", 194, deg(0, 0, 0))
    key(rig, "rotation_euler", 204, deg(0, 0, 0))
    key(rig, "location", 0, (0, -0.006, 0))
    key(rig, "location", 164, (0, 0, 0))
    key(rig, "location", 204, (0, 0, 0))
    # Emerge from darkness: the screen wakes first, then the rim, then the key.
    for name, f0, f1, e in (("rim_r", 18, 70, 34), ("rim_l", 30, 80, 20), ("key", 36, 100, 28), ("fill", 36, 100, 6), ("sweep", 30, 90, 1.4)):
        ld = lights[name].data
        key(ld, "energy", 0, 0.0)
        key(ld, "energy", f0, 0.0)
        key(ld, "energy", f1, e)
    key(glass_bsdf.inputs["Emission Strength"], "default_value", 0, 0.0)
    key(glass_bsdf.inputs["Emission Strength"], "default_value", 6, 0.0)
    key(glass_bsdf.inputs["Emission Strength"], "default_value", 34, SCREEN_GAIN)
    return [cam, rig] + [lights[n].data for n in lights]


def anim_protect(rig, cam, lights, focus):
    cam.data.dof.focus_object = focus
    d = 0.86
    ppm = frame_px_per_m(d)
    off = -380 / ppm  # phone centre at frame x 1340
    # Slow 10 deg orbit around the phone. The camera aims left of the phone so it sits at frame x 1340.
    for f, a in ((1090, -14.0), (1252, -4.0)):
        ar = math.radians(a)
        cam.location = Vector((math.sin(ar) * d, 0.0, math.cos(ar) * d))
        right = Vector((math.cos(ar), 0, -math.sin(ar)))
        look_at(cam, Vector((0, 0.0, 0)) + right * off)
        cam.keyframe_insert("location", frame=f)
        cam.keyframe_insert("rotation_euler", frame=f)
    key(rig, "rotation_euler", 1090, deg(-8, -26, -4))
    key(rig, "rotation_euler", 1252, deg(-7, -26, -3.5))
    key(rig, "location", 1090, (0, -0.010, 0))
    key(rig, "location", 1124, (0, 0, 0))
    key(rig, "location", 1252, (0, 0.003, 0))
    return [cam, rig]


def anim_end(rig, cam, lights, focus):
    cam.data.dof.focus_object = focus
    d = 0.80
    ppm = frame_px_per_m(d)
    cam.location = (-400 / ppm, 0.0, d)
    cam.rotation_euler = (0, 0, 0)
    # Hero turn: 3/4 back (module catching the rim light) to the front, landing on b62 (f1550).
    key(rig, "rotation_euler", 1440, deg(6, 152, -3))
    key(rig, "rotation_euler", 1550, deg(0, -14, 0))
    key(rig, "rotation_euler", 1552, deg(0, -14, 0))
    key(rig, "location", 1440, (0, -0.016, -0.02))
    key(rig, "location", 1550, (0, 0, 0))
    key(rig, "location", 1552, (0, 0, 0))
    return [rig]


def align_table(cam, rig, frames):
    """Per-frame projection of the hook dot and the local screen scale, for the world-map handoff."""
    sc = bpy.context.scene
    out = []
    for f in range(frames[0], frames[1] + 1):
        sc.frame_set(f)
        mw = rig.matrix_world
        pts = [mw @ tex_to_local(540, 1702), mw @ tex_to_local(640, 1702), mw @ tex_to_local(540, 1802)]
        px = []
        for p in pts:
            v = world_to_camera_view(sc, cam, p)
            px.append((v.x * 1920, (1 - v.y) * 1080))
        sx = math.dist(px[0], px[1]) / 100
        sy = math.dist(px[0], px[2]) / 100
        out.append(dict(f=f, x=round(px[0][0], 2), y=round(px[0][1], 2), sx=round(sx, 5), sy=round(sy, 5)))
    return out


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser()
    ap.add_argument("--shot", required=True, choices=list(SHOTS) + ["calibrate"])
    ap.add_argument("--engine", default="eevee", choices=("eevee", "cycles"))
    ap.add_argument("--samples", type=int, default=64)
    ap.add_argument("--scale", type=int, default=100)
    ap.add_argument("--still", type=int, nargs="?", const=-1)
    ap.add_argument("--frames", type=int, nargs=2)
    ap.add_argument("--align", action="store_true")
    ap.add_argument("--out", default=os.path.join(ROOT, "blender", "render"))
    ap.add_argument("--save-blend", action="store_true")
    a = ap.parse_args(argv)
    if a.shot == "calibrate":
        calibrate()
        return
    cfg = SHOTS[a.shot]

    sc = setup_scene(a.engine, a.samples, a.scale)
    rig, glass = build_phone()
    parts = list(rig.children)
    video = os.path.join(ROOT, "blender", "render", "screens", cfg["video"])
    mat, bsdf = screen_material(video, cfg["video_start"], cfg["video_frames"])
    glass.data.materials[0] = mat
    cam = make_camera()
    cam.data.dof.aperture_fstop = cfg["fstop"]
    lights = setup_lights(a.shot, parts, glass)
    focus = bpy.data.objects.new("Focus", None)
    sc.collection.objects.link(focus)
    focus.parent = rig
    focus.location = tex_to_local(540, 1702) if a.shot == "hook" else (0, 0, ZG)

    if a.shot == "hook":
        animated = anim_hook(rig, cam, lights, bsdf, focus)
        animated.append(mat.node_tree)
    elif a.shot == "protect":
        animated = anim_protect(rig, cam, lights, focus)
    else:
        animated = anim_end(rig, cam, lights, focus)
    for idd in animated:
        shape_curves(idd, 0.36 if a.shot == "protect" else 0.6)
    sc.frame_start, sc.frame_end = cfg["frames"]

    if a.save_blend:
        bpy.ops.wm.save_as_mainfile(filepath=os.path.join(a.out, f"{a.shot}.blend"))

    if a.align:
        tab = align_table(cam, rig, (176, 204))
        path = os.path.join(ROOT, "blender", "hook-align.json")
        with open(path, "w") as fh:
            json.dump(tab, fh, indent=1)
        print("ALIGN", path, tab[-5:])
        return

    if a.still is not None:
        f = cfg["still"] if a.still < 0 else a.still
        sc.frame_set(f)
        sc.render.filepath = os.path.join(a.out, "stills", f"{a.shot}-{f:04d}-{a.engine}.png")
        t = time.time()
        bpy.ops.render.render(write_still=True)
        print(f"STILL {a.shot} f{f} {a.engine} {time.time() - t:.2f}s -> {sc.render.filepath}")
        return

    f0, f1 = a.frames if a.frames else cfg["frames"]
    sc.frame_start, sc.frame_end = f0, f1
    sc.render.filepath = os.path.join(a.out, a.shot, "")
    t = time.time()
    bpy.ops.render.render(animation=True)
    n = f1 - f0 + 1
    dt = time.time() - t
    print(f"SEQ {a.shot} {n} frames {a.engine} {dt:.1f}s {dt / n:.2f}s/frame")


main()
