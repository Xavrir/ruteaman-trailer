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

### 1. Hook, 0.00 to 6.67 s (beats 0 to 8)
- **Visual:** a blurred, near-black city map. A phone on the right shows a dark map, the time `22.47` and a white "you are here" dot with two soft pulses.
- **Text:** "Pulang malam?" (b1), then "Jalan mana yang aman?" (b4). The first line then dims to grey.
- **Motion:** the phone rises in. At b7 the camera pushes through the phone screen (scale 5, ease-in), and the full-size map appears at b8.
- **Why:** the screen is the only bright object, so it reads as a phone glowing at night without any glow effect. Dimming the first line moves focus to the real question. The push-through hands the dot to the next shot (the dot stays in the same place on screen).

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
- **Beat A, Pelindung aktif (b44 to b50):** the camera pushes in (1.2x). A white dot travels the mint route, and the stretch already travelled dims behind it. Text: "Pelindung aktif" / "Lokasimu dibagikan langsung ke orang rumah."
- **Beat B, SOS (hard cut at b50):** black. A red SOS button presses (scale 0.93 and back) and sends two red rings outwards. Text: "Tekan SOS, kontak daruratmu diberi tahu."
- **Why:** there are only two beats, per the brief. Transit, hazard reporting and check-in were cut so that the one idea stays clear. The hard cut to SOS is the only abrupt moment in the film. It means "if something goes wrong, help is one tap away", and it is the only red.

### 7. Arrival and end card, 45.00 to 54.17 s (beats 54 to 65)
- **Arrival (hard cut back at b54):** a closer framing on home. The dot finishes the route at b55, the home marker fills with mint and one ring expands. Text: "Sudah sampai." / "Orang rumah sudah dikabari."
- **End card (b58 onward):** the logo and wordmark lockup (b58), "Pulang malam, tetap tenang." (b59), "Rute terang, kabar untuk orang rumah." (b60), and "GEMASTIK 2026 · Universitas Bina Nusantara" (b61). A static hold of 2.5 s ends the film.
- **Why:** the story ends where the promise ends: home, calm, and the family informed. Mint fills the destination, so the brand colour closes the arc. The tagline follows from that image.

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
| Pulang malam, tetap tenang. | 1.8 s | 5.0 s |
