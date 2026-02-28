# Eliot
**Eliot** is a code generation tool that transforms a behavioral specification network behavior into `C++` code. 

The user describes the runtime behavior of network communication using a `DAG` specification file, and **Eliot** generates the corresponding `C++` code. 

The generated code is compiled together with a provided backend. A traits file serves as a linking layer between the generated code and the backend, allowing the generated code use the backend's methods and functions.

---

## Installation
```bash
# Clone the repository
git clone git@github.com:Samo2003/BP.git Eliot
cd Eliot

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Usage
### Print DAG JSON specification
To print the DAG JSON specification run:
```bash
python eliot.py --dag_schema
```


### DAG specification
To define the network target behavior you need to create a `DAG` specification file in `YAML` or `JSON` format. Example files can be found in `example_dags/`. The exact arguments and structures of each node can be found in classes defined in `src/DAG/`.


### Traits Setup
You need to specify a traits file defining a linking layer between your backend and the generated code. The file `traits/TraitsTemplate.hpp` contains required methods together with their explanations. Other files in the `traits/` directory serve as examples.


### Code generation
To generate the code and binary file run:
```bash
python eliot.py \
    --dag <path_to_dag> \
    --traits <path_to_traits_file> \
    --backend <path_to_backend_directory>
```
The generated code will be placed by default in the current directory in the `generated/` folder. You can change the output directory by adding the `--output <path_to_output_directory>` argument to the command above. The result is a generated `C++` code and a compiled binary file `eliot`.

Example of the command:
```bash
python eliot.py \
    --dag example_dags/line_control.yaml \
    --traits traits/EchoTraits.hpp \
    --backend mocks/echo
```

**NOTE**: To run the generator `Ninja` build system must be installed on your computer.

---

## Tests
To execute the tests run:
```bash
pytest -n auto
```