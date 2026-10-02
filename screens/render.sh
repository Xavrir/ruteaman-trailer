#!/usr/bin/env bash
# Render the phone screen compositions and unpack them to JPEG sequences for Blender
# (an image sequence seeks instantly; a movie texture decodes from the last keyframe on every still).
set -euo pipefail
cd "$(dirname "$0")/.."
export PATH="$(ls -d "$HOME"/.nvm/versions/node/v"$(cat .nvmrc)".* | tail -1)/bin:$PATH"
out=blender/render/screens
mkdir -p "$out"
for s in ${@:-a b c}; do
  npx --yes hyperframes@0.8.111 render . -c "screens/screen-$s.html" -o "$out/screen-$s.mp4" -f 30 -q high -w 4 --quiet >/dev/null
  rm -rf "$out/screen-$s" && mkdir -p "$out/screen-$s"
  ffmpeg -v error -i "$out/screen-$s.mp4" -q:v 2 -start_number 1 "$out/screen-$s/%04d.jpg"
  echo "screen-$s: $(ls "$out/screen-$s" | wc -l) frames"
done
