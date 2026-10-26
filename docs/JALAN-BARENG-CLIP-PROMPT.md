# Prompt: RuteAman "Jalan Bareng" motion graphic clip

Copy everything below the line into the agent that will build the clip (Claude Code or Codex, working in `/home/xavrir/ruteaman-trailer`).

---

You are a senior motion designer and a careful engineer. Build a short motion graphic clip that explains the RuteAman feature **Jalan Bareng**. It must look like it belongs to the existing RuteAman trailer (`out/ruteaman-trailer-16x9.mp4`): same palette, same type, same calm product-film motion, same procedural 3D phone. Aim for Apple product-film quality: one idea per beat, the screen as the only bright object, motion that settles instead of wobbling.

## Read first (do not skip)

1. `STORYBOARD.md`: the visual system table, motion rules, colour rules and the 72 BPM beat grid. Follow them exactly.
2. `blender/phone.py` and `blender/render.sh`: the procedural phone, lighting, light linking, Filmic plus the inverse LUT for screens, and the PRIME offload gotcha (EEVEE must run on the RTX 4050, not the iGPU).
3. `screens/screen-a.html`, `screens/screen.css`, `screens/render.sh`: how phone screens are built as HyperFrames compositions (1080x2340, app dark tokens, Inter, 28 pt sheet radius) and rendered to JPEG sequences.
4. `index.html`: how the trailer composes 3D clips (VP9 alpha WebM), text columns and the map.
5. The real app screens for this feature, so the UI on the phone matches the product: `assets/ref/bareng/buddy-verified-dark.png` (the list), `buddy-sheet-verified-dark.png` (the detail sheet with the invite button), `buddy-locked-dark.png` (before the ID check), `verify-camera-review-dark.png` and `verify-demo-approved-dark.png` (the ID check). Copy their layout, row structure, badge style and wording. Do not invent UI the app does not have.
6. Brand assets: `assets/img/logo.png` (RuteAman logo), `assets/mascot/` (Kunang: `Kunang.tsx` and `kunang-poses.ts` hold the vector poses; `kunang-sampai.png` and `kunang-halo.png` are transparent cutouts; `kunang-svg-preview.png` shows every pose).

## What Jalan Bareng is (facts from the app, use only these)

- It shows **teman searah**: other RuteAman users walking to the same destination at about the same time.
- Each row shows a first name, distance and departure time, and a track record, for example: "Sari", "350 m darimu · berangkat 21.10", "Nilai 4,8 · 12 jalan bareng".
- Only users whose identity was checked can invite. The check compares a KTP photo with a selfie using a vision model. The badge text is **"Dicek AI"**. Never write "terverifikasi" or "verified": the app deliberately avoids that claim.
- A user turns on **"Bisa diajak jalan bareng"** to appear for people walking the same route.
- Inviting: the button **"Ajak jalan bareng"** becomes **"Ajakan terkirim"**.
- After the invite is accepted, both share live location: **"Berbagi lokasi langsung"**, with a **"Lihat lokasi"** button.
- Safety exits exist: **"Laporkan ke admin"** and block ("Kalian tidak akan saling muncul lagi di Jalan Bareng").

## Format and deliverables

- 1920x1080, 30 fps, about 20 s (8 shots on the 72 BPM grid: one beat = 25 frames). Silent, music-ready (cuts on beats).
- Deliver:
  1. `out/jalan-bareng-16x9.mp4`: the full clip (H.264, yuv420p, about 8 to 12 MB).
  2. `assets/3d/phone-bareng.webm`: the 3D phone shots only, VP9 with alpha (`yuva420p`, `-auto-alt-ref 0`), transparent background, phone on the right half (x 1040 to 1500) so a pitch deck can put text on the left.
  3. `assets/3d/phone-bareng-once.webm`: the same as (2) but it plays once and then holds the last frame for 240 s (`tpad=stop_mode=clone:stop_duration=240`), because the deck player always loops clips.
  4. `out/stills/bareng-*.png`: one still per shot, plus a contact sheet.
  5. A short `docs/JALAN-BARENG-REPORT.md`: what was built, render times, any deviations and why.

## Visual system (inherit from the trailer)

| Element | Rule |
| --- | --- |
| Base | `#0B0F16` night black, greys from the app dark tokens |
| Mint `#00E6B0` | The only "safe / together" colour. Used for the shared route, the "Dicek AI" badge, the accepted state, the end lockup. |
| Amber `#FF9F0A` | Not used in this clip. |
| Red `#D70015` | Not used in this clip (no SOS beat). |
| Type | Inter Display 700 for headlines (84 to 120 px), Inter 500 for body (40 to 52 px), tabular figures for every number |
| Layout | Text column on the left (x 120 to 880) over a black scrim, phone or map on the right. The same composition in every shot so the eye always knows where to look. |
| Motion | Entrances `power3.out`, camera moves `power4.inOut`. No bounce, no idle breathing, no drift. Everything settles. |
| Effects | Nothing decorative: no particles, lens flares or gradients for show. Light comes from the screen and two thin rim lights. |
| Copy | Formal Indonesian, short. Every line must pass the reading-time check: 3 words per second plus 0.5 s. |

## Subtitles and on-screen text (app-launch trailer style)

All headline text in the shot list below is a subtitle in the style of modern app launch trailers (Apple, Linear, Arc): big, clean, one short line at a time, revealed word by word. Apply this to every line in every shot.

- **Font:** Inter Display, weight 600 for the line and 700 for one emphasis word. Letter spacing -0.02em, line height 1.05. SF Pro is the reference look but is licensed only for Apple platforms, so use Inter Display (already in `assets/fonts/`). No other fonts.
- **Size:** 88 to 104 px for the main line, 44 to 52 px Inter 500 for the small grey support line (`#AEB3BD`). Never smaller than 40 px.
- **Length:** at most 6 words per line and at most 2 lines on screen at once. Split longer sentences across beats.
- **Colour:** white `#F2F4F7`. Exactly one emphasis word per line may be mint `#00E6B0` (for example "**searah**", "**Dicek AI**", "**bareng**"). No outlines, boxes, drop shadows or background plates. Readability comes from the black scrim behind the text column.
- **Position:** left text column (x 120 to 880), vertically centred on the frame, left aligned, in the same place in every shot so it never jumps. In the hook and end card, where there is no phone, keep the same left column (do not centre).
- **Reveal:** word by word. Each word goes from opacity 0, `blur(12px)`, translateY(24px) to opacity 1, blur 0, translateY 0 over 0.5 s with `power3.out`, staggered 70 ms per word. The emphasis word arrives last in its line and takes 0.6 s.
- **Change of line:** the previous line dims to `#5B6472` (as in the trailer) in 0.3 s when the next one starts; it leaves with the shot cut, never by sliding away.
- **Exit:** text cuts with the shot on the beat. No fade-out longer than 0.25 s.
- **Numbers:** tabular figures (`font-variant-numeric: tabular-nums`) so nothing jitters.
- **Timing:** each line stays fully readable for at least its reading time (3 words per second plus 0.5 s) after its last word lands. Add these lines to the reading-time table in the report.

## Shot list (beat numbers are on the 72 BPM grid)

1. **Hook, b0 to b5 (0 to 4.2 s).** Night map (reuse the trailer's desaturated map treatment). Two white dots start far apart and move along their own grey paths; both paths bend toward the same destination marker. Text: "Pulang sendirian?" (b1), then "Ternyata ada yang searah." (b3), first line dims to grey. Why: the problem is loneliness on the walk home, and the map shows the answer before the UI does.
2. **The match, b5 to b10 (4.2 to 8.3 s), 3D shot.** The phone rises on the right with a slow 12 degree yaw turn toward camera. Screen D: the Jalan Bareng page, "Jalan kaki ke Stasiun MRT Bundaran HI", the toggle "Bisa diajak jalan bareng" on, and two rows: "Sari · 350 m darimu · berangkat 21.10 · Nilai 4,8 · 12 jalan bareng" and "Dewi · 600 m darimu · berangkat 21.15 · Nilai 4,9 · 7 jalan bareng", each with a mint "Dicek AI" badge. The rows slide in one by one (b7, b8). Text: "Teman searah, di rute yang sama."
3. **Trust, b10 to b14 (8.3 to 11.7 s), flat graphic.** Phone goes to black. Two line icons (an ID card and a face) slide toward each other and merge into one mint "Dicek AI" badge (the badge from the app, scaled up). Text: "Identitas dicek AI sebelum bisa mengajak." Small grey line under it: "Bisa diblokir dan dilaporkan kapan saja." Why: safety is the reason a stranger is acceptable; show it before the invite.
4. **Invite, b14 to b18 (11.7 to 15.0 s), 3D shot.** Back to the phone (same framing as shot 2, no new camera move). Screen E: the detail sheet for Sari. A soft tap ring on "Ajak jalan bareng"; the button cross-fades to "Ajakan terkirim" with a check (b16). Text: "Satu ketukan untuk mengajak."
5. **Together, b18 to b23 (15.0 to 19.2 s), map.** The phone tilts back and hands off to the map exactly like the trailer's hook push (the phone's map becomes the world map; export the alignment table from Blender the same way as `hook-align.json`). The two dots meet at a corner, then walk as one along a single mint route ribbon. A small pill follows them: "Berbagi lokasi langsung". Text: "Jalan bareng, terpantau sampai tiba."
6. **End card, b23 to b26 hold (19.2 to about 21.7 s).** Map fades. Lockup: RuteAman logo plus "Jalan Bareng" (white) with a mint underline that draws left to right. Tagline: "Pulang bareng, lebih tenang." Kunang (the mascot, "Sampai" pose: rebuild it as SVG from `assets/mascot/kunang-poses.ts`, or use `assets/mascot/kunang-sampai.png`) fades in small at the right. Everything holds still for the last 2 s.

## 3D phone (Blender)

- Reuse `blender/phone.py`; add a `--shot bareng` mode instead of forking the file. Same phone model, materials, lights, light linking and colour pipeline.
- Screens D and E are new HyperFrames compositions (`screens/screen-d.html`, `screens/screen-e.html`) rendered to JPEG sequences, never movie textures (Blender decodes movie textures from the last keyframe on every still).
- Render EEVEE headless on the NVIDIA GPU with the PRIME offload environment from the trailer report (about 1 s per frame; 13 s per frame means it fell back to the iGPU, stop and fix it).

## Honesty rules (non-negotiable)

- Names on screen are sample names only (Sari, Dewi). No real people, no real photos, no real phone numbers.
- Never claim "terverifikasi", "aman 100%", user counts, ratings averages or any statistic. The only numbers on screen are the sample row values above.
- Do not show features the app does not have (no group chat, no in-app calls, no payments).

## Quality gate before you report done

1. `npx hyperframes check` passes (ignore only the known full-frame alpha `text_occluded` infos).
2. Every text line passes the reading-time table; add the table to the report.
3. Extract the alpha WebM's frames at 0.2, 0.5 and 0.98 of its length with `-c:v libvpx-vp9` and confirm the alpha channel exists and the phone bounding box stays inside x 1000 to 1560.
4. Watch the full MP4 once end to end and write down any frame where two elements compete for attention; fix it.
5. Confirm mint is the only accent colour in every still.
