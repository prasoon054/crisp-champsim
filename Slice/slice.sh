#!/bin/bash

# This script takes a binary path as a command-line argument.
# It then reads instruction addresses from 'loads.csv' and sends
# the binary path and each address to 'slicer.py'.

# --- Configuration ---
INPUT_FILE="loads.csv"
SLICER_SCRIPT="slicer.py"

# --- Argument Check ---
if [ -z "$1" ]; then
  echo "Error: No binary path provided."
  echo "Usage: ./slice.sh /path/to/your/binary"
  exit 1
fi

BINARY_PATH="$1"

# --- File Checks ---
if [ ! -f "$BINARY_PATH" ]; then
  echo "Error: Binary '$BINARY_PATH' not found."
  exit 1
fi

if [ ! -f "$INPUT_FILE" ]; then
  echo "Error: Input file '$INPUT_FILE' not found."
  exit 1
fi

if [ ! -f "$SLICER_SCRIPT" ]; then
  echo "Error: Slicer script '$SLICER_SCRIPT' not found."
  exit 1
fi

echo "--- Starting instruction slicing process ---"
echo "Using Binary: $BINARY_PATH"

# 1. 'tail -n +2' skips the multi-line header [cite: 1-7].
# 2. 'awk' extracts only the Code Location (column 1)[cite: 1].
# 3. 'while read' loop assigns this to 'instruction_addr'.
tail -n +2 "$INPUT_FILE" | awk '{print $1}' | while read -r instruction_addr
do
  # Check for a valid-looking address
  if [[ "$instruction_addr" == 0x* ]]; then
    echo "Processing address: $instruction_addr"

    # Run the slicer with the provided Binary Path and the read Address
    python "$SLICER_SCRIPT" "$BINARY_PATH" "$instruction_addr"

  else
    echo "Skipping invalid line: $instruction_addr"
  fi
done

echo "--- Slicing process complete ---"
