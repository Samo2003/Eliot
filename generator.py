import sys
import json
from typing import cast
from src.generator.nf_queue_api import *
from src.DAG import *
from src.test_case import *
from src.generator import generate
import os
import shutil
import click
import subprocess

BUILD_DIR = "build"
BINARY_NAME = "eliot"

def load_dag(dag: str | None, test_case: str | None) -> DAG:
    """
    Loads DAG model directly if provided otherwise loads and translates given test case

    Raises `RuntimeError` if loading fails
    """

    try:
        if dag:
            # Load and validate DAG
            with open(dag, "r") as file:
                data = json.load(file)
                return DAG.model_validate(data)
        else:
            # Load and convert test case into DAG
            test_case_model = load_test_case(cast(str, test_case))
            return translate_to_DAG(test_case_model)
    except Exception as e:
        raise RuntimeError(f"ERROR: loading input file: {e}")

def clear_output_dir(path: str) -> None:
    """Clears the provided repository if it exists and ensures it is created"""
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path, exist_ok=True)

def run_build(keep_build: bool, profiling: bool) -> None:
    """Compiles binary file and moves it to current working directory"""
    os.makedirs(BUILD_DIR, exist_ok=True)
    binary_path = os.path.join(BUILD_DIR, BINARY_NAME)
    cmake_params = ["..", "-DPROFILING=ON"] if profiling else [".."]
    subprocess.run(["cmake"] + cmake_params, cwd=BUILD_DIR, check=True)
    subprocess.run(["make", "-j"], cwd=BUILD_DIR, check=True)
    if not os.path.exists(binary_path):
        raise RuntimeError(f"ERROR: build failed no binary file found")
    
    current_dir = os.getcwd()
    binary = os.path.join(current_dir, BINARY_NAME)
    shutil.copy2(binary_path, binary)

    if not keep_build:
        shutil.rmtree(BUILD_DIR)
    
@click.command()
@click.option("--dag", "-d", type=click.Path(exists=True), help="Path to DAG JSON file")
@click.option("--test_case", "-t", type=click.Path(exists=True), help="Path to test case in JSON or YAML file")
@click.option("--output", "-o", default="./generated/", help="Generator output directory")
@click.option("--templates", default="./templates", help="Path to templates directory")
@click.option("--dag_schema", is_flag=True, help="Print DAG JSON schema and exit")
@click.option("--api", "-a", default="mock", help="Specify NFQueue api type")
@click.option("--keep_build", "-k", is_flag=True, help="If set CMake build directry is not deleted")
def main(dag: str | None, test_case: str | None, output: str, templates: str, dag_schema: bool, api: str, keep_build: bool):
    """Main entry point for generator"""

    if dag_schema:
        print(json.dumps(DAG.model_json_schema(), indent=4))
        sys.exit(0)
    
    if (dag and test_case) or (not dag and not test_case):
        raise click.UsageError("more than 1 or no input file provided")
    
    clear_output_dir(output)

    try:
        dag_model = load_dag(dag, test_case)
        
        profiling = False
        # Determine which NFQueue API is used
        api_interface: NFQueueApiBase
        if api == "mock":
            api_interface = MockApi()
        elif api == "profiling":
            api_interface = ProfilingApi()
            profiling = True
        else:
            raise RuntimeError(f"ERROR: unknown api type: {api}")
        
        generate(dag_model, templates, output, api_interface)

        run_build(keep_build, profiling)
    except RuntimeError as e:
        print(e)
        sys.exit(1)
    except Exception as e:
        print("ERROR: unexpected error in generator")
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
