# RuteAman trailer: report

## Result
- `out/ruteaman-trailer-16x9.mp4`: 1920x1080, 30 fps, 1625 frames, 54.17 s, H.264, yuv420p, no audio, 10.5 MB. It has three 3D phone shots. The earlier flat version is kept as `out/ruteaman-trailer-16x9-flat.mp4` (7.8 MB).
- Render time 28 s (4 workers). Command (Node 22 via `.nvmrc`):
  `npx hyperframes@0.8.111 render . -o out/ruteaman-trailer-16x9.mp4 -f 30 -q high -w 4 --skill=product-launch-video`
- `npx hyperframes check .`: 0 errors, all text WCAG AA. The 12 lint warnings ("use sub-compositions") are deliberate: one map and route camera is shared across five shots.

## Build
HyperFrames 0.8.111. One composition (`index.html`), one paused GSAP 3.14.2 timeline (vendored in `assets/vendor/`, renders offline). Layers: shared night map (`#world`), text scrim, route layer (`#rworld`, SVG routes, ribbons, markers) moving with the same camera, timed text and card clips. Routes are traced on real streets of the app's night-map screenshot and drawn with stroke-dashoffset masks. The logo draws as strokes, then crossfades to the official PNG. Numbers count up in tabular figures with id-ID decimal commas.

Skills read from a shallow clone in `.vendor/` (not installed globally): `hyperframes`, `hyperframes-core`, `product-launch-video`, `motion-graphics`, `hyperframes-cli`.

## 3D phone
- **Tools:** Blender 5.2.0 LTS headless (`blender -b`), EEVEE, 96 samples, 1920x1080 RGBA PNG, Filmic view. EEVEE got a GPU context in background mode, so Cycles was not needed.
- **Speed:** on the Intel iGPU (Blender's default on this muxless Optimus laptop) a 3-frame test took 13 s/frame. With NVIDIA PRIME offload (`blender/render.sh`) the RTX 4050 renders 0.9 to 1.0 s/frame. Final sequences: hook 205 frames 208 s (1.01 s/frame), protection 163 frames 162 s (0.99), end 113 frames 98 s (0.87). Total 3D render 7.8 min. The end clip's 2.4 s hold repeats the settled frame.
- **Clips:** VP9 WebM with alpha (`yuva420p`, CRF 20), 2.6 to 2.9 MB each in `assets/3d/`. A test showed that HyperFrames extracts alpha WebM frames as PNG and blends a semi-transparent pixel correctly over the layers below.
- **Screens:** `screens/screen-{a,b,c}.html`, rendered by `screens/render.sh` (HyperFrames to MP4, then a JPEG sequence, because a movie texture in Blender decodes from the last keyframe on every still, up to 40 s per frame).
- **Commands:** `screens/render.sh`, then `blender/render.sh --shot hook|protect|end --samples 96`, `blender/render.sh --shot hook --align` for the handoff table, `blender/render.sh --shot calibrate` for the colour LUT.
- **Stills:** `blender/render/stills/` (raw RGBA, ignored by git) and `out/stills/3d/` (key frames over black).

### Fixed after the stills
- **Washed-out screens:** the 1.4 m key light reflected in the cover glass and turned the protection screen almost white (and the top of the hook screen). Fixed with light linking: key, rims and fill light only the body; one dim soft strip is the only light in the glass. Its strength went from 5 W to 1.4 W after the first full watch, and on the end card it moved to the right, so it crosses the glass during the turn and leaves the settled screen clear.
- **Colour:** AgX crushed the dark map (code 10 showed as 5) and turned mint pale and amber salmon. Switched to Filmic and added a per-channel inverse LUT: mint, amber, SOS red and the dark greys now render at their token values (white at about 242).
- **Protection framing:** `to_track_quat` assumes Z-up, so the camera rolled 90° and the phone lay sideways. Replaced it with a Y-up look-at; the phone now enters 10 mm lower and settles at frame centre height.
- **Back glass:** read as light silver under the key. Darker base, rougher, lower specular: now dark graphite with a soft gradient.
- **Handoff:** the push now lands at f194 with the dot at (1360, 726), so the world map's bottom edge stays below the frame. The hook shade layer kept darkening the world map until f205; it now fades out with the push. The world map used a blurred hospital label but the phone showed it sharp, so a sharp copy of the map sits on top at b8 and fades to the blurred one over 1 s.
- **Arrival overlap:** the back of the phone appeared over the arrival map at 48.0 s; its fade now starts at f1454, after the map has gone.

## Apple motion guide applied
- One idea: you get home calm because the route is chosen for safety. Protection cut to two beats (Pelindung, SOS).
- Colours: black and greys, mint = safe, amber only inside the ribbon, red only on SOS. Two typefaces (Inter Display, Inter).
- One focal point per shot; transitions grow from the action (push through the phone, the white fastest route returns as the amber ribbon, the safe ribbon becomes the live route, the mint destination leads to the end card). Hard cuts only into and out of SOS.
- 72 BPM beat grid (25 frames per beat); the payoff holds 4 s, the end card 2.5 s.

## Stills and full-watch fixes (flat version)
Greyscale phone map (no red icons); smaller text removed; darker, blurrier hook background; route layer above the scrim; map labels blurred out of the text column with a near-solid scrim; stronger quiet-street darkening; map dimmed to 12% during the payoff; arrival text moved to the headline slot; route points moved onto road centrelines; brand lockup lowered 60 px; "no data" dash 26/16; pulse rings hidden before their animation (`immediateRender: false`); accents snapped to the beat grid. Three full watches at 2 fps contact sheets.

## Notes
The 67,6% and route numbers are the paper's prototype scenario; the payoff says "skenario prototipe". No audio; see `MUSIC.md` for the 72 BPM cut points, track search terms and sound effects.
