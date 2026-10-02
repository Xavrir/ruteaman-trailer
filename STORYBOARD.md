# RuteAman trailer: storyboard

One idea: **you get home calm, because the route is chosen for safety.**
1920x1080, 30 fps, 54.17 s (1625 frames). The cut grid is 72 BPM: one beat = 25 frames = 0.833 s, and every shot starts on a beat.

## Visual system (applies to every shot)

| Element | Choice | Reason |
| --- | --- | --- |
| Colours | Black and dark greys, white type, mint `#00E6B0` for "safe" | Night setting. Mint is the brand colour and the only thing that says "safe". |
| Amber `#FF9F0A` | Only inside the risk ribbon | It marks risky stretches. It is never used for UI or text. |
| Red `#D70015` | Only the SOS button | It stays the single urgent colour, so the SOS shot hits hard. |
| Grey dashes | Ribbon stretches with too little data | Same convention as the app. |
| Type | Inter Display 700 for titles (84 to 120 px), Inter 500 for body (40 to 52 px), tabular figures for all numbers | Two faces only. Numbers do not jitter while they count. |
| Layout | Text in a left column (x 120 to 880), the map and route on the right, a black scrim under the text | The same composition from the problem shot to the arrival shot, so the eye always knows where to look. |
| Map | Real night map from the app (`home-night-z15.png`), desaturated, 50% brightness. The large "Rumah Sakit Umum Kecamatan Tanah Abang" label is blurred out of the source. The route overlay is a separate layer above the text scrim | Real product material. Muted so that the route is the brightest thing in the frame. No map label competes with our text, and the scrim never dims the route. |
| Motion | Entrances use `power3.out`. Camera moves use `power4.inOut`. There is no bounce, no loop breathing and no back-half drift | Calm and confident. Elements settle; they do not wobble. |
| Effects | None decorative. No glow, particles or gradients for show | Attention comes from contrast and from what moves. |

## Shots

### 1. Hook, 0.00 to 6.67 s (beats 0 to 8), 3D shot 1
- **Visual:** a blurred, near-black city map. A 3D phone on the right (Screen A: night map, `22.47`, white "you are here" dot with two pulses, collapsed sheet "Cari tujuan atau alamat").
- **Text:** "Pulang malam?" (b1), then "Jalan mana yang aman?" (b4). The first line then dims to grey.
- **Motion:** the screen wakes first (f6 to f34), then the rim light catches the frame edge, then the soft key fills it in. The phone turns 15° toward the camera (yaw -28° to -13°) over the shot. From f164 the camera pushes into the dot (`power4.inOut`-like Bezier) and lands at f194; the sheet and map controls slide away on the screen during the push. The world map fades in under the phone and the bezel dissolves (f186 to f202), then the map settles to its problem-shot framing from b8.
- **Why:** the screen is the only bright object, so it reads as a phone glowing at night without any glow effect. The 3/4 turn gives the phone a physical presence before the story moves into the map. The phone's map *is* the world map: Blender exports the dot position and screen scale for every frame of the push (`blender/hook-align.json`), and `index.html` places the world map on the same pixels, so the map seems to spill out of the screen at b8.

### 2. Problem, 6.67 to 13.33 s (beats 8 to 16)
- **Visual:** the map settles from 1.15x to 1.0x. A plain white route (an ordinary map app's fastest route) draws from the dot to home through back streets. That area darkens. Pills: "Jalan sepi, minim lampu" (b11) and "13 mnt" (b12).
- **Text:** "Aplikasi peta memilih yang tercepat." (b1 of the shot), then "Bukan yang teraman." (b13) with the first line dimmed.
- **Motion:** stroke-dashoffset draw (`power2.inOut`, 2 s). At about 12.8 s everything dims to black, just before the b16 cut.
- **Why:** white, not mint, because this is not our route. The darkened area is the visual proof of the claim. The dip to black is a silent beat before the answer.

### 3. RuteAman, 13.33 to 17.50 s (beats 16 to 21)
- **Visual:** on black, the logo draws itself as mint strokes (shield, R, two pins). It then crossfades to the official PNG. The wordmark "Rute" (white) and "Aman" (mint) rises in at b18.
- **Why:** the logo is made of route-like strokes, so drawing it repeats the route-line motif. The crossfade keeps the final mark pixel-exact.

### 4. How it works, 17.50 to 26.67 s (beats 21 to 32)
- **Visual:** the same map and framing as shot 2. The safe route draws as a risk ribbon: mint, with one amber stretch and one grey dashed stretch. The pills "Waspada" (b24) and "Data kurang" (b25) appear as the ribbon reaches those stretches. At b27 the headline changes and four factor rows appear one at a time: Laporan warga, Jalan gelap, Sepi & jam rawan, Jarak ke bantuan (line icons on dark tiles).
- **Text:** "Setiap ruas jalan dinilai risikonya.", then "Dari empat sinyal."
- **Why:** the labels sit on the ribbon itself rather than in a legend, so the viewer reads them where they look. The factors arrive one by one in the second half of the shot, not all at once. Icons are white so that mint keeps one meaning.

### 5. The choice, 26.67 to 36.67 s (beats 32 to 44)
- **Visual:** the fastest route from shot 2 comes back, now drawn as a ribbon (mostly amber). Two cards slide in on the left:
  - **Rute Aman** (mint border; 22 in mint): Risiko 22, 1,4 km, 18 mnt, "Lewat jalan terang dan ramai."
  - **Rute Tercepat**: Risiko 68, 1,1 km, 13 mnt.

  All numbers count up in tabular figures.
- **Payoff (b39, held 3.8 s):** the map drops to 12%. Center text: "+5 menit," / "risiko turun **67,6%**" (the number counts up in mint), with "Selisih 0,3 km · skenario prototipe" below.
- **Why:** the same white line from shot 2 now shows its true risk. That is the turn of the story. The payoff is the longest hold in the film after the end card, because it is the claim to remember. The small note keeps the number honest: it is a prototype scenario and a relative risk.

### 6. Protection, 36.67 to 45.00 s (beats 44 to 54)
- **Beat A, Pelindung aktif (b44 to b50), 3D shot 2:** the map goes to black and a 3D phone floats in on the right with a gentle tilt (pitch -8°, roll -4°) and a slow 10° camera orbit. Screen B shows navigation: the mint risk ribbon with its traveled part dimmed and a moving dot, a "Belok kiri" banner counting 250 to 190 m, and a bottom sheet with "7 mnt", "Pelindung aktif", "Bagikan" and a small red SOS. The left text column is unchanged: "Pelindung aktif" / "Lokasimu dibagikan langsung ke orang rumah."
- **Beat B, SOS (hard cut at b50):** black. A red SOS button presses (scale 0.93 and back) and sends two red rings outwards. Text: "Tekan SOS, kontak daruratmu diberi tahu."
- **Why:** there are only two beats, per the brief. Showing protection on the product itself (not on the abstract map) says "this is the app you hold"; the phone over black keeps one focal point next to the text. Transit, hazard reporting and check-in were cut so that the one idea stays clear. The hard cut to SOS is the only abrupt moment in the film. It means "if something goes wrong, help is one tap away", and it is the only red.

### 7. Arrival and end card, 45.00 to 54.17 s (beats 54 to 65)
- **Arrival (hard cut back at b54):** a closer framing on home. The dot finishes the route at b55, the home marker fills with mint and one ring expands. Text: "Sudah sampai." / "Orang rumah sudah dikabari."
- **End card, 3D shot 3 (f1440 to the end):** as the map fades, the phone turns from a 3/4 back view (the camera island and lens rings catch the rim light) through 166° to the front with Screen C: route options with "Rute Aman 22" selected (mint), "Rute Tercepat 68" and a mint "Mulai" button. It settles on b62 (f1550) on the right. The text column on the left: lockup (b59), "Pulang malam, / tetap tenang." (b60), "Rute terang, kabar untuk orang rumah.", and "GEMASTIK 2026 · Universitas Bina Nusantara" (b61). Everything is still for the last 2.4 s.
- **Why:** the story ends where the promise ends: home, calm, and the family informed. Mint fills the destination, so the brand colour closes the arc. The tagline follows from that image.

## 3D phone (Blender)

| Shot | Film frames | Screen | Camera and phone |
| --- | --- | --- | --- |
| Hook | 0 to 204 | A: night map, dot, collapsed sheet | 3/4 turn of 15°, push into the dot, lands f194 |
| Protection | 1090 to 1250 | B: navigation, ribbon, banner, Pelindung bar | Gentle tilt, 10° orbit |
| End card | 1440 to 1625 | C: route options, Mulai | Hero turn back to front, settles b62, holds |

There is no fourth shot: tilting the phone into the map would repeat the hook handoff.

- **Phone:** generic, procedural (`blender/phone.py`). 72.5 x 152 x 8 mm, 10 mm corners, a satin graphite aluminium frame with a smooth chamfer, flat cover glass with thin even bezels (0.9 mm lip + 1.3 mm black border), a centred punch-hole, volume and power keys on the right edge, a USB-C slot, and a back camera island with two lenses and a flash. No brand's distinctive shapes.
- **Screens:** three HyperFrames compositions in `screens/` (1080x2340, 30 fps, the app's dark tokens, a 28 pt sheet radius, Inter). They play as image-sequence textures on the glass through exact planar UVs: the active area has the texture's 1080:2340 aspect, so nothing stretches.
- **Look:** a large soft key, two thin rims on the frame edges, a dim fill, no coloured lights. One soft strip is the only light the screen glass reflects (light linking), so reflections cross the glass as a gentle sweep and never wash out the UI. Filmic view transform, motion blur, f/2.8 to f/3.2 depth of field focused on the screen.
- **Colour:** Filmic would dim and shift the UI, so the screen shader runs each channel through an inverse Filmic LUT (`blender/view-inverse.json`). Mint, amber and SOS red display at their token values.

## Reading-time check (3 words per second + 0.5 s)

| Text | Needed | On screen |
| --- | --- | --- |
| Jalan mana yang aman? | 1.8 s | 2.3 s |
| Aplikasi peta memilih yang tercepat. | 2.2 s | 5.6 s |
| Bukan yang teraman. | 1.5 s | 1.9 s |
| Setiap ruas jalan dinilai risikonya. | 2.2 s | 4.2 s |
| Factor rows (9 words) | 3.5 s | 3.5 s (first row) to 2.3 s (last row) |
| Route cards (about 12 words) | 4.5 s | 4.8 s |
| +5 menit, risiko turun 67,6% | 2.2 s | 3.8 s |
| Lokasimu dibagikan langsung ke orang rumah. | 2.5 s | 3.3 s |
| Tekan SOS, kontak daruratmu diberi tahu. | 2.5 s | 2.5 s |
| Pulang malam, tetap tenang. | 1.8 s | 4.2 s |
