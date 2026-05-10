# Mock Backends
[Back to main README](../README.md#traits-setup)

This directory contains simple backend implementations used for testing,
examples, benchmarking, and profiling generated fault models.

Each backend exposes the queue-like interface expected by Eliot through a
matching traits file in `traits/`.

| Backend | Traits file | Purpose |
|---------|-------------|---------|
| `mock/` | `traits/MockTraits.hpp` | Configurable UDP link used by the example sender/receiver scripts. |
| `echo/` | `traits/EchoTraits.hpp` | Minimal UDP echo backend used for `pytest`. |
| `benchmark/` | `traits/BenchmarkTraits.hpp` | Synthetic packet source for throughput benchmarks. |
| `profiling/` | `traits/ProfilingTraits.hpp` | Synthetic packet source for profiler-oriented runs. |
