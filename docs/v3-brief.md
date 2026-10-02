# Trailer v3 brief: real app screens, 3D phone for the route story, award-level craft

## Goals (user, 2026-10-02)
1. The phone screens show the REAL latest app build (Plan 3 shell: persistent night map, explore sheet, search, route options with the risk ribbon), recorded from the app, not mock HTML.
2. The route part of the story (current shots 4 and 5: risk ribbon, four signals, route choice 22 vs 68) is shown INSIDE the 3D phone, like the intro, instead of the flat full-frame map.
3. Raise the craft to the level of a "best motion graphics" award entry, within the Apple motion guide (one idea, restraint, contrast not glow, max 3 colours, 2 typefaces, overlapping eased motion, beat-locked cuts).

## Step A: build and record the real app (do not touch the user's repo or phone)
- Clone: `git clone --local /home/xavrir/ruteaman-app /home/xavrir/ruteaman-trailer-app && cd /home/xavrir/ruteaman-trailer-app && git checkout 6fd4ef3` (detached is fine). Copy `/home/xavrir/ruteaman-app/.env` into the clone (it holds the live API URL; never print it). `npm ci`, then `npx expo prebuild --platform android` (Node 20 via nvm default; the app is Expo SDK 56).
- Build: `cd android && JAVA_HOME=/usr/lib/jvm/java-17-openjdk PATH=/usr/lib/jvm/java-17-openjdk/bin:$PATH ./gradlew assembleRelease -PreactNativeArchitectures=x86_64`.
- Emulator: `~/Android/Sdk/emulator/emulator -avd Pixel_7_API_35 -no-snapshot-save -no-audio &`; only `adb -s emulator-5554`. NEVER connect to or install on the physical phone (192.168.100.x). Set dark mode for night scenes (`cmd uimode night yes`) and a Jakarta GPS fix (`adb -s emulator-5554 emu geo fix 106.8135 -6.2005`, Tanah Abang area). Hide the status bar clutter with demo mode (`settings put global sysui_demo_allowed 1`, then `am broadcast -a com.android.systemui.demo -e command clock -e hhmm 2247`, battery full, wifi full, notifications off). Restore uimode, demo mode and animation scales afterwards.
- Use guest mode. Record real flows with `adb shell screenrecord --size 1080x2400 --bit-rate 20M` (max 3 min per file):
  - S1 explore: the map at night with the location dot, sheet at medium (search field, Keamanan rows), a slow sheet drag down to collapsed.
  - S2 search: tap search, type a destination (e.g. "Monas" or "Blok M"), results appear, pick one.
  - S3 route options: car or walk mode, the camera fits, the risk ribbon draws, alternatives grey; tap an alternative and the selection swaps; mode switch Jalan to Mobil.
  - S4 (protection): the current navigation screen after "Mulai" (it is the older navigation UI until Plan 3b; use it only if it looks good, else keep the existing designed Screen B for Pelindung and say so).
  - Pick routes that show visible amber stretches; try 2 or 3 destinations at night to find one with a clear mint/amber ribbon.
  Record several takes; choose the smoothest. Trim with ffmpeg; keep 1080x2400 (or crop/scale to the phone screen aspect in the Blender model; adjust the model's screen aspect to 1080:2400 = 9:20 if needed, or letterbox nothing: fill exactly).
- Screens must be truthful: real app, real data. Do not fake UI that the app does not have. Short speed-ups (1.5x to 2x) of waiting are fine; no fake numbers. The 22/68 and 67,6% figures stay as the paper's prototype scenario in the flat payoff, labelled "skenario prototipe"; the phone shows whatever the real app shows.

## Step B: 3D phone story for the route part
- Replace the flat-map shots 4 and 5 with 3D phone shots that show the real recordings: e.g. (1) the phone turns into a 3/4 hero angle as S3 plays and the ribbon draws on its screen; (2) a slow push towards the screen as the user taps the alternative; (3) a match-cut or pull-out to the flat payoff "+5 menit, risiko turun 67,6%" (keep the payoff typographic and full-frame: it is the claim to remember).
- The four signals (Laporan warga, Jalan gelap, Sepi & jam rawan, Jarak ke bantuan) can float as clean typographic labels beside the phone, revealed on beats, not on the map.
- Hook: replace the mock Screen A with real S1 if it reads well at that size; keep the push-into-screen handoff idea but hand off into the real recording rather than the old flat map if that is stronger.
- End card: the hero turn shows real S3 (route options) on screen.
- Re-render the Blender shots with the real screen textures (Eevee via blender/render.sh, the NVIDIA path). Keep render time reasonable (measure s/frame; under ~60 min total).

## Step C: award-level polish (judge your own frames against this list)
- Camera language: every 3D move is motivated, eased with real F-curves, ends on a beat; vary shot sizes (wide, medium, extreme close-up of the screen glass and frame edge); at least one macro detail shot of the phone frame catching the rim light.
- Depth and light: soft studio key, crisp rim, subtle floor reflection or contact shadow where the phone is near a surface; motion blur on fast moves; gentle depth of field on close-ups. No lens flares, no bloom glow.
- Type: kinetic but restrained: words reveal with masks or per-line rises on beats; tabular numbers; Inter Display titles tight-tracked; perfect kerning and alignment to a grid.
- Transitions: match cuts between flat and 3D (the route line on the flat map continues into the route on the phone screen, or the screen fills the frame and becomes the flat shot).
- Rhythm: build energy in the middle, hold the payoff and the end; total length 50 to 60 s; keep the 72 BPM grid.
- Colour: night palette; consider a very dark blue-black base (around #0B1220 to #0E1116) instead of neutral black for a calmer night feel; mint only for safe; red only SOS. Optionally the arrival and end card shift to a warm off-white (#F5F3EF) to express relief; decide by looking at frames, and keep it only if it is clearly better.
- Sound: still no audio track; update MUSIC.md cut points if timing changes.
- Watch the full film as a 2 fps contact sheet after every render; fix weak frames. Do at least two full review passes.

## Deliverables
- `out/ruteaman-trailer-16x9.mp4` (new v3); keep v2 as `out/ruteaman-trailer-16x9-v2-3d.mp4` and the flat one as is.
- Updated STORYBOARD.md, MUSIC.md, REPORT.md (what was recorded, which takes, Blender/Eevee timings, review passes and fixes).
- Commit in ~/ruteaman-trailer with plain messages (no AI mention, no trailers). Keep big recordings out of git except the final trimmed screen clips the film needs (if over ~20 MB total, use git-ignored `assets/screens-real/` plus a script that regenerates them, and say so).
- Leave ~/ruteaman-trailer-app in place (it can be deleted later).
