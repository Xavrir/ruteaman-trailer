// Shared route data for the phone screens. Points are map-wide.jpg pixels (the
// trailer's world map); map-tall.jpg is the same source 620 px taller.
window.RA = (() => {
  const NS = "http://www.w3.org/2000/svg";
  const MINT = "#00e6b0", AMBER = "#ff9f0a", UNKNOWN = "#8e8e93";
  const TALL = 620;
  const START = [735, 860];
  const DEST = [1400, 305];
  const SAFE = [
    [START, MINT], [[757, 740], MINT], [[782, 640], MINT], [[808, 520], MINT], [[834, 450], MINT],
    [[950, 440], MINT], [[1150, 480], MINT], [[1190, 486], AMBER], [[1350, 503], MINT],
    [[1550, 518], MINT], [[1612, 523], MINT], [[1612, 440], UNKNOWN], [[1612, 352], MINT],
    [[1612, 305], MINT], [DEST, null],
  ];
  const FAST = [START, [860, 852], [990, 850], [990, 700], [990, 560], [990, 415], [1350, 415], [1350, 305], DEST];

  function roundedPath(pts, r = 26) {
    let d = `M${pts[0][0]},${pts[0][1]}`;
    for (let i = 1; i < pts.length - 1; i++) {
      const [px, py] = pts[i - 1], [cx, cy] = pts[i], [nx, ny] = pts[i + 1];
      const l1 = Math.hypot(cx - px, cy - py), l2 = Math.hypot(nx - cx, ny - cy);
      const k1 = Math.min(r, l1 / 2) / l1, k2 = Math.min(r, l2 / 2) / l2;
      d += ` L${cx - (cx - px) * k1},${cy - (cy - py) * k1} Q${cx},${cy} ${cx + (nx - cx) * k2},${cy + (ny - cy) * k2}`;
    }
    const last = pts[pts.length - 1];
    return d + ` L${last[0]},${last[1]}`;
  }

  function el(tag, attrs, parent) {
    const n = document.createElementNS(NS, tag);
    for (const k in attrs) n.setAttribute(k, attrs[k]);
    parent.appendChild(n);
    return n;
  }

  function ribbon(group, w = 24) {
    const pts = SAFE.map((p) => p[0]);
    const d = roundedPath(pts);
    el("path", { d, fill: "none", stroke: "#050506", "stroke-width": w + 16, "stroke-linecap": "round", "stroke-linejoin": "round" }, group);
    let i = 0;
    while (i < SAFE.length - 1) {
      const color = SAFE[i][1];
      let j = i + 1;
      while (j < SAFE.length - 1 && SAFE[j][1] === color) j++;
      const attrs = { d: roundedPath(pts.slice(i, j + 1)), fill: "none", stroke: color, "stroke-width": w, "stroke-linecap": color === UNKNOWN ? "butt" : "round", "stroke-linejoin": "round" };
      if (color === UNKNOWN) attrs["stroke-dasharray"] = "30 18";
      el("path", attrs, group);
      i = j;
    }
    return el("path", { d, fill: "none", stroke: "none" }, group);
  }

  function dot(parent, x, y, core = 26, halo = 64) {
    const g = el("g", { transform: `translate(${x} ${y})` }, parent);
    el("circle", { r: halo, fill: "#fff", "fill-opacity": 0.16 }, g);
    el("circle", { r: core, fill: "#fff", stroke: "#0c0c0d", "stroke-width": core * 0.36 }, g);
    return g;
  }

  return { NS, MINT, AMBER, UNKNOWN, TALL, START, DEST, SAFE, FAST, roundedPath, el, ribbon, dot };
})();
