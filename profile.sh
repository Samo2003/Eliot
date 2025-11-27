#!/bin/bash

set -e

MODE="${1:-linux}"   # default = linux

OUTPUT_DIR="profiling_output"
mkdir -p "$OUTPUT_DIR"

if [[ "$MODE" == "clean" ]]; then
    rm -rf "$OUTPUT_DIR"
    rm -rf perf.data perf.trace out.perf profile.txt user_profile.txt
    exit 0
fi

# Run the program
./eliot &
ELIOT_PID=$!

if [[ "$MODE" == "mac" ]]; then
    rm -rf perf.trace

    xctrace record \
        --template "Time Profiler" \
        --time-limit 10s \
        --attach $ELIOT_PID \
        --output perf.trace

    kill -SIGINT $ELIOT_PID
    wait $ELIOT_PID || true

    rm -rf "$OUTPUT_DIR/perf.trace"
    mv perf.trace "$OUTPUT_DIR/"
    open "$OUTPUT_DIR/perf.trace"
elif [[ "$MODE" == "linux" ]]; then
    perf record -F 999 -g -p $ELIOT_PID -- sleep 20

    kill -SIGINT $ELIOT_PID
    wait $ELIOT_PID || true

    perf script -i perf.data > "$OUTPUT_DIR/profile.txt"
    perf script -i perf.data | grep -v "\\[kernel.kallsyms\\]" > "$OUTPUT_DIR/user_profile.txt"
    rm -f perf.data
    # https://www.speedscope.app - open either file here
else
    echo "Unknown mode: $MODE"
    echo "Usage: ./profile.sh [mac|linux|clean]"
    exit 1
fi
