#!/bin/bash

./eliot &
PID=$!

rm -rf perf.trace

xctrace record \
    --template "Time Profiler" \
    --time-limit 10s \
    --attach $PID \
    --output perf.trace

kill -SIGINT $PID

wait $PID

open perf.trace
