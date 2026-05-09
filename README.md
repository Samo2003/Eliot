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

For development purposes install with development dependencies:
```bash
pip install -e ".[dev]"
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

### DAG specification
To define the network target behavior you need to create a `DAG` specification file in `YAML` or `JSON` format. Example files can be found in `example_dags/`. The exact arguments and structures of each node can be found in classes defined in `src/eliot/DAG/`.

### Traits Setup
You need to specify a traits file defining a linking layer between your backend and the generated code. The file `traits/TraitsTemplate.hpp` contains required methods together with their explanations. Other files in the `traits/` directory serve as examples.

### Code generation
To generate the code and binary file, run:
```bash
eliot generate \
    --dag <path_to_dag> \
    --traits <path_to_traits_file> \
    --backend <path_to_backend_directory>
```
The generated code will be placed by default in the current directory in the `generated/` folder. You can change the output directory by adding the `--output <path_to_output_directory>` argument to the command above. The result is a generated `C++` code and a compiled binary file `eliot-run`.

Example of the command:
```bash
eliot generate \
    --dag example_dags/line_control.yaml \
    --traits traits/MockTraits.hpp \
    --backend mocks/mock
```

---

## Tests
To execute the tests run:
```bash
pytest -n auto
```

The tests are located in the `tests/` directory. They consist of end-to-end tests to verify the complete generation and execution pipeline. Each test consists of generating code from DAG specification, building a binary file, sending defined packet sequences and validating the provided constraints.

---

## Notes
Some source code comments were generated using [`ChatGPT`](https://chat.openai.com).