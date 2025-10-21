#!/bin/bash
if [ "$#" -lt 2 ]; then
    echo "Usage: ./build-trace.sh <num_of_instructions> <path_to_binary>"
    exit 1
fi
NUM_INST="$1"
BINPATH="$2"
if [ "$#" -gt 2 ]; then
    BIN_ARGS=("$(@:3)")
else
    BIN_ARGS=()
fi
BINPATH="$(realpath "$BINPATH")"
if [ ! -f "$BINPATH" ]; then
    echo "ERROR: Binary not found at: $BINPATH"
    exit 1
fi
if [ ! -x "$BINPATH" ]; then
    echo "WARNING: $BINPATH is not executable. Attempting to continue."
fi
CHAMPSIM_ROOT="$(pwd)/ChampSim"
TRACER_DIR="$CHAMPSIM_ROOT/tracer/pin"
if [ ! -d "$TRACER_DIR" ]; then
    echo "ERROR: tracer/pin directory not found"
    exit 1
fi
if [ -z "${PIN_ROOT:-}" ]; then
    echo "ERROR: PIN_ROOT environment variable is not set."
    exit 1
fi
echo "Building tracer in: $TRACER_DIR"
pushd "$TRACER_DIR" >/dev/null
make
popd >/dev/null
TRACER_SO="$TRACER_DIR/obj-intel64/champsim_tracer.so"
if [ ! -f "$TRACER_SO" ]; then
    echo "ERROR: tracer shared object not found at: $TRACER_SO"
    exit 1
fi
mkdir -p "$CHAMPSIM_ROOT/traces"
BIN_NAME="$(basename "$BINPATH")"
OUTFILE="$CHAMPSIM_ROOT/traces/${BIN_NAME}_trace.champsim"
if [ -e "$OUTFILE" ]; then
    read -p "Warning: $OUTFILE already exists. It will be overwritten. Continue? [y/N]" user_input
    user_input=$(echo "$user_input" | tr '[:upper:]' '[:lower:]')
    if [[ "$user_input" != "y" ]]; then
        echo "Exitted."
        exit 0
    fi
fi
"$PIN_ROOT/pin" -t "$TRACER_SO" -o "$OUTFILE" -s 0 -t "$NUM_INST" -- "$BINPATH" "${BIN_ARGS[@]:-}"
RET=$?
if [ $RET -ne 0 ]; then
    echo "ERROR: pin returned non-zero exit code: $RET"
    exit $RET
fi
read -p "Compress the trace? [y/N]" user_input
user_input=$(echo "$user_input" | tr '[:upper:]' '[:lower:]')
if [[ "$user_input" != "y" ]]; then
    echo "Exitted"
    exit 0
fi
xz -k $OUTFILE
