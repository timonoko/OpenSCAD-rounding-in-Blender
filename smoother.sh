#!/usr/bin/env bash
set -euo pipefail

# ==============================================================================
# smoother.sh
# Runs Blender in headless/background mode to import, remesh, smooth,
# and save an STL mesh using openscad_prep2.py.
#
# Usage:
#   ./smoother.sh [input_stl] [output_stl]
#
# Examples:
#   ./smoother.sh
#       Imports parturi.stl and writes parturi_smoothed.stl
#
#   ./smoother.sh parturi.stl parturi.stl
#       Overwrites parturi.stl in-place
#
#   ./smoother.sh input.stl output.stl
#       Smooths input.stl and saves to output.stl
# ==============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/openscad_prep2.py"

# Default input to parturi.stl
if [ -n "${1:-}" ]; then
    INPUT_FILE="$1"
elif [ -f "parturi.stl" ]; then
    INPUT_FILE="parturi.stl"
else
    INPUT_FILE="$SCRIPT_DIR/parturi.stl"
fi

# Default output: if 2nd arg provided, use it; otherwise save as <name>_smoothed.stl
if [ -n "${2:-}" ]; then
    OUTPUT_FILE="$2"
else
    DIRNAME="$(dirname "$INPUT_FILE")"
    BASENAME="$(basename "$INPUT_FILE")"
    FILENAME="${BASENAME%.*}"
    OUTPUT_FILE="${DIRNAME}/${FILENAME}_smoothed.stl"
fi

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
echo "============================================="

blender --background --python "$PYTHON_SCRIPT" -- "$INPUT_FILE" "$OUTPUT_FILE"

echo "============================================="
echo "Successfully generated: $OUTPUT_FILE"
echo "============================================="
