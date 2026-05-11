# Tests

[Back to main README](../README.md#tests)

End-to-end tests are in `tests/cases/`. Each test case is stored in its own directory and must contain two files:

```text
tests/cases/<category>/<case_name>/
  config.yaml
  assert.py
```

`config.yaml` describes the generated model and the packets to send. The `build` field can contain either a DAG (`root: ...`) or a test-case rule model (`defaultAction` and `rules`). The `send` field describes the sequence of packets to send to the generated binary. The `timeout` field specifies the maximum time to wait for the test to complete, in seconds after sending all packets. This is useful when testing actions such as `Delay`.

Minimal example:

```yaml
name: Drop UDP packets
timeout: 0.1

build:
  root:
    condition: { type: Protocol, id: 17 }
    if_true:
      action: { type: Drop }
    if_false:
      action: { type: Finish }

send:
  - protocol: udp
    count: 5
```

Packet send steps support fields such as:

| Field | Default | Description |
|-------|---------|-------------|
| `protocol` | `raw` | `udp`, `tcp`, `icmp`, or `raw` |
| `protocol_id` | `99` | IP protocol number for `raw` packets |
| `src`, `dst` | `10.10.10.1`, `10.10.10.2` | Packet IP addresses |
| `count` | `1` | Number of packets for this step |
| `payload_size` | `256` | Payload size in bytes |
| `payload` | `null` | Optional payload value with encoding |
| `sport`, `dport` | `12345`, `54321` | TCP/UDP ports |
| `icmp_type`, `icmp_code` | `8`, `0` | ICMP fields |
| `delay` | `null` | Delay before this step, in milliseconds |
| `interval` | `0` | Delay between packets, in milliseconds |

`assert.py` must define a `check(stats: ExchangeStats) -> None` function. Use plain `assert` statements inside it.

Minimal example:

```python
from tests.stats import ExchangeStats

def check(stats: ExchangeStats) -> None:
    assert stats.sent_count == 5
    assert stats.received_count == 0
```

Useful `ExchangeStats` attributes:

| Attribute | Description |
|-----------|-------------|
| `sent_count` | Number of packets sent by the test runner |
| `received_count` | Number of packets received back from generated code |
| `sent` | List of sent packet records |
| `received` | List of received packet records |
| `exchanges` | Sent packets paired with matching responses by sequence number |
| `extra` | Received packets that did not match a sent sequence number |
| `no_losses` | True when every sent packet has a response |

Run all tests in parallel with:

```bash
pytest -n auto
```

Use `--clean` when generated build outputs should be recreated:

```bash
pytest --clean -n auto
```
