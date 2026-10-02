# RuteAman trailer: report

## Result
- `out/ruteaman-trailer-16x9.mp4`: 1920x1080, 30 fps, 1625 frames, 54.17 s, H.264 High, yuv420p, no audio, 7.8 MB.
- Render time 24.8 s (4 workers). Command (Node 22 via `.nvmrc`):
  `npx hyperframes@0.8.111 render . -o out/ruteaman-trailer-16x9.mp4 -f 30 -q high -w 4 --skill=product-launch-video`
- `npx hyperframes check .`: 0 errors, all text WCAG AA. The 12 lint warnings ("use sub-compositions") are deliberate: one map and route camera is shared across five shots.

## Build
HyperFrames 0.8.111. One composition (`index.html`), one paused GSAP 3.14.2 timeline (vendored in `assets/vendor/`, renders offline). Layers: shared night map (`#world`), text scrim, route layer (`#rworld`, SVG routes, ribbons, markers) moving with the same camera, timed text and card clips. Routes are traced on real streets of the app's night-map screenshot and drawn with stroke-dashoffset masks. The logo draws as strokes, then crossfades to the official PNG. Numbers count up in tabular figures with id-ID decimal commas.

Skills read from a shallow clone in `.vendor/` (not installed globally): `hyperframes`, `hyperframes-core`, `product-launch-video`, `motion-graphics`, `hyperframes-cli`.

## Apple motion guide applied
- One idea: you get home calm because the route is chosen for safety. Protection cut to two beats (Pelindung, SOS).
- Colours: black and greys, mint = safe, amber only inside the ribbon, red only on SOS. Two typefaces (Inter Display, Inter).
- One focal point per shot; transitions grow from the action (push through the phone, the white fastest route returns as the amber ribbon, the safe ribbon becomes the live route, the mint destination leads to the end card). Hard cuts only into and out of SOS.
- 72 BPM beat grid (25 frames per beat); the payoff holds 4 s, the end card 2.5 s.

## Stills and full-watch fixes
Greyscale phone map (no red icons); smaller text removed; darker, blurrier hook background; route layer above the scrim; map labels blurred out of the text column with a near-solid scrim; stronger quiet-street darkening; map dimmed to 12% during the payoff; arrival text moved to the headline slot; route points moved onto road centrelines; brand lockup lowered 60 px; "no data" dash 26/16; pulse rings hidden before their animation (`immediateRender: false`); accents snapped to the beat grid. Three full watches at 2 fps contact sheets.

## Notes
The 67,6% and route numbers are the paper's prototype scenario; the payoff says "skenario prototipe". No audio; see `MUSIC.md` for the 72 BPM cut points, track search terms and sound effects.
