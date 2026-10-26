import type { MascotColors } from '../tokens/colors';

/**
 * Kunang, the RuteAman firefly, as hand-authored line art on a 120 x 120 grid.
 * Pure data and string helpers only (no React Native imports), so the Node tests
 * and scripts/render-kunang-preview.mjs read the same shapes the app draws.
 */
export type KunangPose = 'halo' | 'sampai' | 'tidur' | 'berpikir' | 'waspada';

export const VIEWBOX = 120;
const MID = VIEWBOX / 2;

/** Every outline uses STROKE; FINE is only for the chest mark, which is a badge, not a limb. */
export const STROKE = 3.8;
export const FINE = 1.7;

export type Fill = 'none' | 'ink' | 'wing';
export type Width = 'main' | 'fine' | 'none';

export type Shape =
  | { kind: 'path'; d: string; fill?: Fill; width?: Width }
  | { kind: 'circle'; cx: number; cy: number; r: number; fill?: Fill; width?: Width }
  | { kind: 'ellipse'; cx: number; cy: number; rx: number; ry: number; fill?: Fill; width?: Width };

export interface PoseGeometry {
  /** Degrees, clockwise, about the grid centre. */
  rotate: number;
  halo: { cx: number; cy: number; r: number };
  core: { cx: number; cy: number; rx: number; ry: number };
  wings: Shape[];
  body: Shape[];
  eyes: Shape[];
  /** Drawn unrotated, on top: check badge, question mark, sleep marks, motion ticks. */
  extras: Shape[];
  /** Point the wings flap about, before rotation. */
  wingHinge: [number, number];
}

export interface PoseMotion {
  blink: boolean;
  flutter: boolean;
  settle: boolean;
}

export interface PoseEntry {
  label: string;
  geometry: PoseGeometry;
  motion: PoseMotion;
}

const path = (d: string, fill: Fill = 'none', width: Width = 'main'): Shape => ({ kind: 'path', d, fill, width });
const ring = (cx: number, cy: number, r = 3.6): Shape => ({ kind: 'circle', cx, cy, r, fill: 'none', width: 'main' });
const dot = (cx: number, cy: number, r = 2.9): Shape => ({ kind: 'circle', cx, cy, r, fill: 'ink', width: 'none' });

/** Mirrors an absolute-command path across the vertical centre line. */
export function mirror(d: string): string {
  const tokens = d.match(/[MLHVCQAZ]|-?\d*\.?\d+/g) ?? [];
  const out: string[] = [];
  let cmd = '';
  let i = 0;
  const num = () => Number(tokens[i++]);
  const fx = (x: number) => +(VIEWBOX - x).toFixed(2);
  while (i < tokens.length) {
    const t = tokens[i];
    if (/[A-Z]/.test(t)) {
      cmd = t;
      i++;
      out.push(cmd);
      if (cmd === 'Z') continue;
    }
    switch (cmd) {
      case 'M':
      case 'L':
        out.push(`${fx(num())} ${num()}`);
        break;
      case 'H':
        out.push(`${fx(num())}`);
        break;
      case 'V':
        out.push(`${num()}`);
        break;
      case 'Q':
        out.push(`${fx(num())} ${num()} ${fx(num())} ${num()}`);
        break;
      case 'C':
        out.push(`${fx(num())} ${num()} ${fx(num())} ${num()} ${fx(num())} ${num()}`);
        break;
      case 'A': {
        const [rx, ry, rot, large, sweep] = [num(), num(), num(), num(), num()];
        out.push(`${rx} ${ry} ${-rot} ${large} ${sweep ? 0 : 1} ${fx(num())} ${num()}`);
        break;
      }
      default:
        throw new Error(`mirror: unsupported command ${cmd}`);
    }
  }
  return out.join(' ');
}

const both = (d: string, fill: Fill = 'none'): Shape[] => [path(d, fill), path(mirror(d), fill)];

const head: Shape = { kind: 'ellipse', cx: 60, cy: 40, rx: 20.5, ry: 19, fill: 'none', width: 'main' };
const antennae: Shape[] = [...both('M53 22.2 C51.6 16.4 48.6 12.6 45 10.6'), ring(41.7, 8.8), ring(78.3, 8.8)];
const hood = path('M44.4 49.4 C41.4 41.2 43.6 31.4 51 26.4');
const bodyFront = path('M51.8 57.4 C45.6 63 44.6 73.4 47.4 82.4 C50.2 91.4 55.4 97.6 60 100.6 C64.6 97.6 69.8 91.4 72.6 82.4 C75.4 73.4 74.4 63 68.2 57.4');
const tailBand = path('M48.2 82.6 Q60 88.2 71.8 82.6');
const mark: Shape[] = [
  path('M55 63.4 Q60 61.8 65 63.4 V68.6 Q65 73.2 60 75.8 Q55 73.2 55 68.6 Z', 'none', 'fine'),
  path('M58.1 72.4 V66.2 H60.8 Q62.6 66.2 62.6 67.9 Q62.6 69.6 60.8 69.6 H58.1 M60.6 69.6 L62.6 72.2', 'none', 'fine'),
];
const lowUpper = 'M47.4 64 C37.6 58.4 22.2 58.6 18.6 66 C15.4 72.6 27.6 76.4 45.8 70.4';
const lowLower = 'M45.8 72.4 C37.4 75.4 29.6 83 32.6 89.6 C35.6 95.4 43.6 88 47.4 79.6';
const upUpper = 'M47.4 63.2 C38.4 48.6 22.4 42.4 15.8 49.4 C9.8 56 19.4 69.2 45.7 68.6';
const upLower = 'M45.6 71.2 C35.4 71 24.6 77.4 26.2 86 C27.8 93.8 40.4 87.6 46.6 78';
const wingsFront: Shape[] = [...both(upUpper, 'wing'), ...both(upLower, 'wing')];
/** Standard wings on the left, low wings on the right: room for a raised right arm. */
const wingsRightLow: Shape[] = [path(upUpper, 'wing'), path(upLower, 'wing'), path(mirror(lowUpper), 'wing'), path(mirror(lowLower), 'wing')];
const wingsLow: Shape[] = [...both(lowUpper, 'wing'), ...both(lowLower, 'wing')];
const frontCore = { cx: 60, cy: 90.4, rx: 10.4, ry: 9.4 };
const frontHalo = { cx: 60, cy: 90.4, r: 27 };
const openEyes = [dot(52.8, 41.4, 3.1), dot(67.2, 41.4, 3.1)];

const halo: PoseGeometry = {
  rotate: 8,
  halo: frontHalo,
  core: frontCore,
  wings: wingsRightLow,
  body: [
    head,
    hood,
    ...antennae,
    bodyFront,
    tailBand,
    ...mark,
    path('M72.6 63.6 C80.6 61.6 86.6 54.6 88.6 44.6'),
    path('M55.6 48.4 Q60 52.4 64.4 48.4'),
  ],
  eyes: openEyes,
  extras: [path('M93.4 30.4 Q97.6 35.6 96.4 42'), path('M99.6 25.2 Q105.4 33 103.8 41.6')],
  wingHinge: [60, 66],
};

const sampai: PoseGeometry = {
  rotate: 0,
  halo: frontHalo,
  core: frontCore,
  wings: wingsLow,
  body: [
    head,
    hood,
    ...antennae,
    bodyFront,
    tailBand,
    ...mark,
    ...both('M47.4 64.2 C41.4 61.6 36.8 56.2 34.6 49.4'),
    path('M54.6 47.6 Q60 54 65.4 47.6'),
  ],
  eyes: [path('M49.2 43 Q52.8 38.2 56.4 43'), path(mirror('M49.2 43 Q52.8 38.2 56.4 43'))],
  extras: [ring(99, 22, 10), path('M94.2 22.2 L97.6 25.6 L103.8 19')],
  wingHinge: [60, 66],
};

const tidur: PoseGeometry = {
  rotate: 0,
  halo: { cx: 32, cy: 76, r: 26 },
  core: { cx: 32.4, cy: 75.6, rx: 8.6, ry: 9.6 },
  wings: [
    path('M58.4 59.4 C53 43 37.4 36.6 30 42.6 C23.6 48 32.6 59.6 55.2 62.4', 'wing'),
    path('M57.2 60.6 C49.4 50.6 38.6 48.6 34.8 53.6 C31.6 58.2 40.4 62.6 54.6 62.6', 'wing'),
  ],
  body: [
    { kind: 'ellipse', cx: 76, cy: 66, rx: 18.5, ry: 17, fill: 'none', width: 'main' },
    path('M73.6 49.2 C73.8 41.8 74.8 36.4 76.6 31.6'),
    ring(77.9, 28.1),
    path('M90 55.6 C95.6 52.4 100.2 54.2 101.6 59.4'),
    ring(102.6, 63),
    path('M59.6 58.8 C52 57.2 44 58.6 36.6 62.4 C26 67.8 22.6 79.6 31 86 C38 91.2 52 87.6 61.6 76.6'),
    path('M42.4 60.8 C37.2 68.4 37.6 80 43.8 88.6'),
    path('M74.4 73.2 Q75.8 74.6 77.2 73.2'),
  ],
  eyes: [path('M65.6 67 Q68.8 70.4 72 67'), path('M79.2 67 Q82.4 70.4 85.6 67')],
  extras: [path('M87 30 H94 L87 37 H94'), path('M98 13 H107 L98 22 H107')],
  wingHinge: [52, 61],
};

const berpikir: PoseGeometry = {
  rotate: -4,
  halo: frontHalo,
  core: frontCore,
  wings: wingsRightLow,
  body: [
    head,
    hood,
    ...antennae,
    bodyFront,
    tailBand,
    ...mark,
    path('M72.8 63.8 C80.4 63.6 81.4 57.4 74.6 55.2'),
    path('M57.2 49.2 Q60.6 51 63.8 48.8'),
  ],
  eyes: [dot(54.2, 39.8, 3.1), dot(68.2, 39.8, 3.1)],
  extras: [path('M88.6 19.6 Q88.6 12.6 94.6 12.6 Q100.6 12.6 100.6 18.6 Q100.6 23 95.6 25 Q94.6 25.6 94.6 29'), dot(94.6, 36, 2.6)],
  wingHinge: [60, 66],
};

const waspada: PoseGeometry = {
  rotate: 0,
  halo: frontHalo,
  core: frontCore,
  wings: wingsFront,
  body: [
    head,
    hood,
    ...antennae,
    bodyFront,
    tailBand,
    ...mark,
    ...both('M46.8 66 Q47.2 74.4 53.4 78.6'),
    path('M55.6 48.4 Q60 51.8 64.4 48.4'),
  ],
  eyes: openEyes,
  extras: [...both('M31.8 24.4 L35.8 28'), ...both('M29 34.4 H34')],
  wingHinge: [60, 66],
};

export const KUNANG_POSES: Record<KunangPose, PoseEntry> = {
  halo: { label: 'Halo', geometry: halo, motion: { blink: true, flutter: true, settle: false } },
  sampai: { label: 'Sampai', geometry: sampai, motion: { blink: false, flutter: false, settle: true } },
  tidur: { label: 'Tidur', geometry: tidur, motion: { blink: false, flutter: false, settle: false } },
  berpikir: { label: 'Berpikir', geometry: berpikir, motion: { blink: true, flutter: false, settle: false } },
  waspada: { label: 'Waspada', geometry: waspada, motion: { blink: true, flutter: false, settle: false } },
};

export const POSE_ORDER: KunangPose[] = ['halo', 'sampai', 'tidur', 'berpikir', 'waspada'];

/** Breathing period of the tail glow, one full in and out. */
export const BREATHE_MS = 3000;
export const BLINK_EVERY_MS = 4200;
export const FLUTTER_EVERY_MS = 2600;
// Off the breathe period on purpose, so the float and the glow drift in and out of step like a live firefly.
export const HOVER_MS = 4400;

/** How far Kunang floats up at the top of its hover, in points: a hint of flight, never a bounce. */
export function hoverLift(size: number): number {
  return Math.round(size * 0.025 * 10) / 10;
}

export interface KunangMotionPlan {
  breathe: boolean;
  blink: boolean;
  flutter: boolean;
  settle: boolean;
}

/** Which loops run. Reduced motion keeps the pose still: no loops and no entrance. */
export function kunangMotionPlan(pose: KunangPose, reduced: boolean, enter = true): KunangMotionPlan {
  if (reduced) return { breathe: false, blink: false, flutter: false, settle: false };
  const m = KUNANG_POSES[pose].motion;
  return { breathe: true, blink: m.blink, flutter: m.flutter, settle: m.settle && enter };
}

/** Stroke width in device pixels at a given rendered size. */
export function strokePx(size: number, width: Width = 'main'): number {
  if (width === 'none') return 0;
  return ((width === 'fine' ? FINE : STROKE) * size) / VIEWBOX;
}

function rotatePoint([x, y]: [number, number], deg: number): [number, number] {
  const a = (deg * Math.PI) / 180;
  const dx = x - MID;
  const dy = y - MID;
  return [MID + dx * Math.cos(a) - dy * Math.sin(a), MID + dx * Math.sin(a) + dy * Math.cos(a)];
}

function shapeCenter(s: Shape): [number, number] {
  if (s.kind !== 'path') return [s.cx, s.cy];
  const n = (s.d.match(/-?\d*\.?\d+/g) ?? []).map(Number);
  const xs = n.filter((_, k) => k % 2 === 0);
  const ys = n.filter((_, k) => k % 2 === 1);
  return [(Math.min(...xs) + Math.max(...xs)) / 2, (Math.min(...ys) + Math.max(...ys)) / 2];
}

const pct = (v: number) => `${+((v / VIEWBOX) * 100).toFixed(2)}%`;

export type Origin = [string, string];

/** Transform origins (as % of the box) for the blink, the wing flap and the glow, after the pose rotation. */
export function motionOrigins(pose: KunangPose): { eyes: Origin; wings: Origin; glow: Origin } {
  const g = KUNANG_POSES[pose].geometry;
  const centers = g.eyes.map((e) => rotatePoint(shapeCenter(e), g.rotate));
  const ex = centers.reduce((s, c) => s + c[0], 0) / centers.length;
  const ey = centers.reduce((s, c) => s + c[1], 0) / centers.length;
  const [wx, wy] = rotatePoint(g.wingHinge, g.rotate);
  const [gx, gy] = rotatePoint([g.halo.cx, g.halo.cy], g.rotate);
  return { eyes: [pct(ex), pct(ey)], wings: [pct(wx), pct(wy)], glow: [pct(gx), pct(gy)] };
}

export function paintFor(s: Shape, colors: MascotColors) {
  const width = s.width ?? 'main';
  return {
    fill: s.fill === 'ink' ? colors.ink : s.fill === 'wing' ? colors.wing : 'none',
    fillOpacity: s.fill === 'wing' ? colors.wingOpacity : 1,
    stroke: width === 'none' ? 'none' : colors.ink,
    strokeWidth: width === 'none' ? 0 : width === 'fine' ? FINE : STROKE,
  };
}

function shapeMarkup(s: Shape, colors: MascotColors): string {
  const p = paintFor(s, colors);
  const paint = `fill="${p.fill}" fill-opacity="${p.fillOpacity}" stroke="${p.stroke}" stroke-width="${p.strokeWidth}" stroke-linecap="round" stroke-linejoin="round"`;
  if (s.kind === 'path') return `<path d="${s.d}" ${paint}/>`;
  if (s.kind === 'circle') return `<circle cx="${s.cx}" cy="${s.cy}" r="${s.r}" ${paint}/>`;
  return `<ellipse cx="${s.cx}" cy="${s.cy}" rx="${s.rx}" ry="${s.ry}" ${paint}/>`;
}

/** Plain SVG for previews and tests; the app draws the same layers with react-native-svg. */
export function kunangSvgMarkup(pose: KunangPose, colors: MascotColors, size = VIEWBOX, id = 'k'): string {
  const g = KUNANG_POSES[pose].geometry;
  const turn = g.rotate ? ` transform="rotate(${g.rotate} ${MID} ${MID})"` : '';
  const shapes = (list: Shape[]) => list.map((s) => shapeMarkup(s, colors)).join('');
  return [
    `<svg xmlns="http://www.w3.org/2000/svg" width="${size}" height="${size}" viewBox="0 0 ${VIEWBOX} ${VIEWBOX}">`,
    '<defs>',
    `<radialGradient id="${id}-halo"><stop offset="0" stop-color="${colors.halo}" stop-opacity="${colors.haloOpacity}"/><stop offset="1" stop-color="${colors.halo}" stop-opacity="0"/></radialGradient>`,
    `<radialGradient id="${id}-core"><stop offset="0" stop-color="${colors.core}" stop-opacity="1"/><stop offset="0.55" stop-color="${colors.core}" stop-opacity="0.9"/><stop offset="1" stop-color="${colors.coreEdge}" stop-opacity="${colors.coreEdgeOpacity}"/></radialGradient>`,
    '</defs>',
    `<g${turn}>`,
    `<circle cx="${g.halo.cx}" cy="${g.halo.cy}" r="${g.halo.r}" fill="url(#${id}-halo)"/>`,
    shapes(g.wings),
    `<ellipse cx="${g.core.cx}" cy="${g.core.cy}" rx="${g.core.rx}" ry="${g.core.ry}" fill="url(#${id}-core)"/>`,
    shapes(g.body),
    shapes(g.eyes),
    '</g>',
    shapes(g.extras),
    '</svg>',
  ].join('');
}
