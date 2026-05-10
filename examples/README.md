# Examples

[go-back](../README.md#examples)

This directory contains DAG examples and two helper scripts for trying them with the `mocks/mock` backend.

The demo topology is:

```text
sender.py -> eliot-run -> receiver.py
```

`backend_config.json` defines the UDP ports used by the mock backend and by the helper scripts. Most of the time you only need to change sender options such as protocol, packet count, IP addresses, or ports of the sent packets.

## Basic workflow

Generate an executable for one DAG:

```bash
eliot generate \
    --dag examples/dags/drop_every_second.yaml \
    --traits traits/MockTraits.hpp \
    --backend mocks/mock
```

Start the generated binary:

```bash
./eliot-run examples/backend_config.json
```

Start the receiver in another terminal:

```bash
python examples/receiver.py
```

Send packets from a third terminal:

```bash
python examples/sender.py --count 10
```

## Sender options

| Option | Default | Description |
|--------|---------|-------------|
| `--count` | `1` | Number of packets to send |
| `--protocol` | `icmp` | Packet protocol: `icmp`, `udp`, `tcp`, or `raw` |
| `--src-ip` | `10.200.0.1` | Source IP written into the generated packet |
| `--dst-ip` | `10.200.0.2` | Destination IP written into the generated packet |
| `--sport` | `12345` | Source port for UDP/TCP packets |
| `--dport` | `12345` | Destination port for UDP/TCP packets |

Examples:

```bash
python examples/sender.py --count 10 --protocol icmp
python examples/sender.py --count 10 --protocol udp --dport 80
python examples/sender.py --count 10 --protocol tcp --sport 12345 --dport 80
python examples/sender.py --count 10 --dst-ip 10.200.0.99
```

The sender puts a readable payload like `packet-0`, `packet-1`, ... into each
packet. The receiver prints this payload, which is useful for observing reorder
or replication behavior.

## Receiver options

The receiver usually works with defaults:

```bash
python examples/receiver.py
```

Useful options:

| Option | Default | Description |
|--------|---------|-------------|
| `--timeout` | `30.0` | How long to wait for packets |

The bind address and port are read from `examples/backend_config.json`.

## Scenario DAGs

| DAG | Description |
|-----|-------------|
| [drop_every_second.yaml](dags/drop_every_second.yaml) | Drops every second packet. |
| [delay_all.yaml](dags/delay_all.yaml) | Delays every packet using a sequence-based delay generator. |
| [reorder_udp.yaml](dags/reorder_udp.yaml) | Reorders UDP packets in groups of five using reverse order. Use `--protocol udp --count 10`. |
| [replicate_udp.yaml](dags/replicate_udp.yaml) | Duplicates UDP packets. Use `--protocol udp` and compare sent vs. received count. |
| [tcp_and_port_80.yaml](dags/tcp_and_port_80.yaml) | Drops TCP packets where source or destination port is `80`. Use `--protocol tcp --dport 80`. |
| [stochastic_drop.yaml](dags/stochastic_drop.yaml) | Randomly drops about 30 percent of packets. |
| [stochastic_delay.yaml](dags/stochastic_delay.yaml) | Applies random delay and then probabilistic drop. |
| [stochastic.yaml](dags/stochastic.yaml) | Demonstrates probabilistic branching with random generators. |
| [line_control.yaml](dags/line_control.yaml) | Uses payload commands `ACTIVE`, `DELAY`, and `DROP` to change runtime state. |
