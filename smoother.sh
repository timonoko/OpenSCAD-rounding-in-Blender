#!/usr/bin/env bash
set -euo pipefail

# ==============================================================================
# smoother.sh
# Runs Blender in headless/background mode to import, remesh, smooth,
# and save an STL mesh using openscad_prep2.py.
#
# Usage:
#   ./smoother.sh [input_stl] [output_stl] [voxel_size]
#
# ==============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/openscad_prep2.py"

# Default input to parturi.stl
    INPUT_FILE="$1"
    OUTPUT_FILE="$2"
    VOXEL_SIZE="$3"

if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: Input STL file '$INPUT_FILE' not found!" >&2
    exit 1
fi

if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "Error: Blender Python script '$PYTHON_SCRIPT' not found!" >&2
    exit 1
fi

echo "============================================="
echo "Smoothing STL with Blender"
echo "  Input:  $INPUT_FILE"
echo "  Output: $OUTPUT_FILE"
echo "  VOXEL_SIZE: $VOXEL_SIZE"
echo "============================================="

blender --background --python "$PYTHON_SCRIPT" -- "$INPUT_FILE" "$OUTPUT_FILE" "$VOXEL_SIZE"

echo "============================================="
echo "Successfully generated: $OUTPUT_FILE"
echo "============================================="

stl-viewer $OUTPUT_FILE
