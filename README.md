# Eliot
**Eliot** is a code generation tool for network fault injection.  

It transforms a declarative behavioral network specification defined as a `DAG`, into `C++` code that is compiled into a standalone tool. The generated code is compiled together with a provided backend implementation. A traits file provides the linking layer between the generated code and the backend, allowing the generated model to interact with the fault injector backend.

---

## Installation
**Requirements:** Python >= 3.10, Ninja build system, C++20 compiler, CMake.
```bash
# Clone the repository
git clone https://github.com/Samo2003/Eliot.git
cd Eliot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install .
```

For development install with development dependencies:
```bash
pip install -e ".[dev]"
```

You can install the required system dependencies on Ubuntu using:
```bash
sudo apt update
sudo apt install python3 python3-venv g++ cmake ninja-build
```

---

## Usage
The following commands assume that the virtual environment is activated.

### Available Commands

| Command | Description |
|--------|-------------|
| `generate` | Generate pipeline code using a custom backend and traits file |
| `benchmark` | Generate code using the benchmark backend |
| `profile` | Generate code configured for profiling |
| `test` | Generate code using the testing backend |
| `schema` | Print the JSON schema for DAG specifications |

**Note:** The `benchmark`, `profile`, and `test` commands only work with editable installation (`pip install -e ".[dev]"`), as they rely on example backends and traits included in the repository.

### Options for the `generate` Command
| Option | Default | Description |
|--------|---------|-------------|
| `-d \| --dag` | None | Path to the DAG specification file (YAML or JSON) |
| `-t \| --traits` | None | Path to the traits file (C++ header) |
| `-b \| --backend` | None | Path to the backend directory containing CMakeLists.txt |
| `-o \| --output` | `.` | Path to the output directory for generated code and binary file |
| `-h \| --help` | None | Show help message and exit |

### DAG specification
To define the target network behavior you need to create a `DAG` specification file in `YAML` or `JSON` format. Example files can be found in `examples/dags/`. The exact arguments and structures of each node can be found in classes defined in `src/eliot/DAG/`.

### Traits Setup
You need to specify a traits file defining an adapter layer between your backend and the generated code. The file `traits/TraitsTemplate.hpp` contains required methods together with their explanations. Other files in the `traits/` directory serve as examples.

The repository also contains several lightweight backend implementations in `mocks/`. See [mocks/README.md](mocks/README.md) for a short overview.

### Code generation
To generate the code and binary file, run:
```bash
eliot generate \
    --dag <path_to_dag> \
    --traits <path_to_traits_file> \
    --backend <path_to_backend_directory>
```
The generated code will be placed by default in the current directory under `generated/`, and the compiled binary will be copied to `./eliot-run`. You can change the output directory by adding the `--output <path_to_output_directory>` argument to the command above.

### Examples
Example of the `generate` command:
```bash
eliot generate \
    --dag examples/dags/drop_every_second.yaml \
    --traits traits/MockTraits.hpp \
    --backend mocks/mock
```

This command generates code for a DAG specification that drops every second packet, using a mock backend and traits file. The target behavior can be tested using the following commands:

In **terminal 1** execute `eliot-run` to start the generated binary:
```bash
./eliot-run examples/backend_config.json
```
**Note:** The `examples/backend_config.json` file contains the configuration for ports and `IP` addresses of the mock backend, which is used in this example.

In **terminal 2** execute the receiver script to accept packets:
```bash
python examples/receiver.py
```

In **terminal 3** execute the sender script to send packets:
```bash
python examples/sender.py --count 10
```

This will send 10 `ICMP` packets from the sender to the receiver. The generated code will drop every second packet, so only 5 packets will be received by the receiver. You can modify the DAG specification to change the behavior or test different scenarios.

For more details about the example scripts and available scenario DAGs, see [examples/README.md](examples/README.md).

---

## Tests
To execute the tests run:
```bash
pytest -n auto
```

The tests are located in the `tests/` directory. They consist of end-to-end tests to verify the complete generation and execution pipeline. Each test consists of generating code from DAG specification, building a binary file, sending defined packet sequences and validating the provided constraints.

If you execute the tests without required system dependencies installed, first install them and then rerun the tests using the `--clean` flag to ensure that all generated code is removed and regenerated with the new dependencies:
```bash
pytest --clean -n auto
```

**Note:** For normal test execution, use the first mentioned command as it results in a faster test execution by reusing `CMake` build files.

---

## Notes
Some source code comments were generated using [`ChatGPT`](https://chat.openai.com).
