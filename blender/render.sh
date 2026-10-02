#!/usr/bin/env bash
# Run phone.py headless on the NVIDIA GPU. The laptop is muxless Optimus; without PRIME offload
# Blender's EEVEE context lands on the Intel iGPU and renders about 2.5x slower.
# Usage: blender/render.sh --shot hook --frames 0 204   (any phone.py options)
set -euo pipefail
cd "$(dirname "$0")/.."
export __NV_PRIME_RENDER_OFFLOAD=1 __GLX_VENDOR_LIBRARY_NAME=nvidia
export __EGL_VENDOR_LIBRARY_FILENAMES=/usr/share/glvnd/egl_vendor.d/10_nvidia.json
exec blender -b --factory-startup -P blender/phone.py -- "$@"
