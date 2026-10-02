"""Cut the real app recordings into the screen clips the 3D shots play.

  python3 screens-real/prep.py clips   screens-real/raw/*.mp4 -> assets/screens-real/<shot>.mp4 (edit list below)
  python3 screens-real/prep.py frames  assets/screens-real/<shot>.mp4 -> blender/render/screens/<shot>/NNNN.jpg

A clip's frame 1 is the 3D shot's first film frame, so Blender maps texture frames 1:1 onto film frames.
The frames step masks the panel corners and the punch-hole so the recording sits inside the glass.
"""

import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EDITS = os.path.join(ROOT, "screens-real", "edits.json")
CLIPS = os.path.join(ROOT, "assets", "screens-real")
FRAMES = os.path.join(ROOT, "blender", "render", "screens")
REC = os.path.join(ROOT, "screens-real", "raw")
W, H = 1080, 2400
# Same physical corner radius as the old screens (7.8 mm on the panel) at the 1080:2400 panel width.
CORNER = 127
HOLE = (540, 62, 21)


def run(*args):
    subprocess.run(args, check=True)


def segment_filter(i, seg):
    """One edit-list entry: [file, in_s, out_s, speed] or ["hold", seconds] (repeats the previous frame)."""
    src, t0, t1, speed = seg
    pts = f"(PTS-STARTPTS)/{speed}"
    return f"[{i}:v]trim={t0}:{t1},setpts={pts},fps=30,scale={W}:{H},setsar=1,format=yuv420p[s{i}]"


def clips(names):
    with open(EDITS) as fh:
        edits = json.load(fh)
    os.makedirs(CLIPS, exist_ok=True)
    for shot, spec in edits.items():
        if names and shot not in names:
            continue
        segs = spec["segments"]
        inputs, filters, labels = [], [], []
        for i, seg in enumerate(segs):
            inputs += ["-i", os.path.join(REC, seg[0])]
            filters.append(segment_filter(i, seg))
            labels.append(f"[s{i}]")
        chain = ";".join(filters) + ";" + "".join(labels) + f"concat=n={len(segs)}:v=1:a=0[cat]"
        frames = spec["frames"]
        # Pad by holding the last frame, then cut to the exact shot length.
        chain += f";[cat]tpad=stop_mode=clone:stop=300,trim=end_frame={frames}[v]"
        out = os.path.join(CLIPS, f"{shot}.mp4")
        run("ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", chain, "-map", "[v]",
            "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-pix_fmt", "yuv420p", "-an", out)
        print(f"{shot}: {frames} frames -> {out}")


def mask_png():
    from PIL import Image, ImageDraw

    path = os.path.join(FRAMES, "mask.png")
    s = 4
    im = Image.new("L", (W * s, H * s), 0)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, W * s - 1, H * s - 1), radius=CORNER * s, fill=255)
    x, y, r = HOLE
    d.ellipse(((x - r) * s, (y - r) * s, (x + r) * s, (y + r) * s), fill=0)
    im = im.resize((W, H), Image.LANCZOS).convert("RGB")
    os.makedirs(FRAMES, exist_ok=True)
    im.save(path)
    return path


def frames(names):
    mask = mask_png()
    for fn in sorted(os.listdir(CLIPS)):
        shot = fn[:-4]
        if not fn.endswith(".mp4") or (names and shot not in names):
            continue
        out = os.path.join(FRAMES, shot)
        run("rm", "-rf", out)
        os.makedirs(out)
        run("ffmpeg", "-v", "error", "-i", os.path.join(CLIPS, fn), "-loop", "1", "-i", mask, "-filter_complex",
            "[0:v]format=gbrp[a];[1:v]format=gbrp[m];[a][m]blend=all_mode=multiply:shortest=1,format=yuvj444p",
            "-q:v", "2", "-start_number", "1", os.path.join(out, "%04d.jpg"))
        print(f"{shot}: {len(os.listdir(out))} frames")


if __name__ == "__main__":
    cmd, names = sys.argv[1], sys.argv[2:]
    {"clips": clips, "frames": frames}[cmd](names)
