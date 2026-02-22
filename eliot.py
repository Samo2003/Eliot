import sys
import json
from typing import cast
from src.DAG import *
from src.test_case import *
from src.generator import generate
import os
import shutil
import click
import subprocess

BINARY_NAME = "eliot"
TEMPLATE_DIR = "./templates"

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
        shutil.rmtree(path, ignore_errors=True)
    os.makedirs(path, exist_ok=True)

def run_build(clear_build: bool, profiling: bool, testing: bool, output: str, generated_dir: str, traits: str, backend: str) -> None:
    """Compiles binary file and moves it to current working directory"""
    build_dir = os.path.join(output, "build")
    os.makedirs(build_dir, exist_ok=True)
    source_root = os.path.abspath(os.path.dirname(__file__))
    cmake_args = [
        "cmake",
        "-G", "Ninja",
        "-S", source_root,
        "-B", build_dir,
        f"-DGENERATED_DIR={generated_dir}",
        f"-DTRAITS_DIR={os.path.dirname(os.path.abspath(traits))}",
        f"-DBACKEND_DIR={os.path.abspath(backend)}"
    ]

    if profiling:
        cmake_args.append("-DPROFILING=ON")

    if testing:
        cmake_args.append("-DTESTING=ON")

    if not testing or not os.path.exists(os.path.join(build_dir, "CMakeCache.txt")):
        subprocess.run(cmake_args, check=True)
    
    build_args = [
        "cmake",
        "--build", build_dir
    ]

    if not testing:
        build_args.append("--parallel")
    subprocess.run(build_args, check=True)

    binary = os.path.join(build_dir, BINARY_NAME)
    if not os.path.exists(binary):
        raise RuntimeError(f"ERROR: build failed no binary file found")
    
    shutil.copy2(binary, output)

    if clear_build:
        shutil.rmtree(build_dir)
    
@click.command()
@click.option("--dag", "-d", type=click.Path(exists=True), help="Path to DAG JSON file")
@click.option("--test_case", "-t", type=click.Path(exists=True), help="Path to test case in JSON or YAML file")
@click.option("--output", "-o", default=".", help="Generator output directory")
@click.option("--dag_schema", "-s", is_flag=True, help="Print DAG JSON schema and exit")
@click.option("--traits", type=click.Path(exists=True), help="Path to trait file for backed")
@click.option("--backend", type=click.Path(exists=True), help="Path to directory containing CMakeLists.txt for backend")
@click.option("--profiling", '-p', is_flag=True, help="Build generated for profiling")
@click.option("--testing", is_flag=True, help="Build generated for testing")
@click.option("--clear_build", "-c", is_flag=True, help="If set CMake build directory is deleted")
def main(dag: str | None, test_case: str | None, output: str, dag_schema: bool, traits: str, backend: str, profiling: bool, testing: bool, clear_build: bool):
    """Main entry point for generator"""

    if dag_schema:
        print(json.dumps(DAG.model_json_schema(), indent=4))
        sys.exit(0)
    
    if (dag and test_case) or (not dag and not test_case):
        raise click.UsageError("more than 1 or no input file provided")
    
    generated_dir = os.path.join(output, "generated")
    clear_output_dir(generated_dir)

    try:
        dag_model = load_dag(dag, test_case)
        
        generate(dag_model, TEMPLATE_DIR, generated_dir, os.path.basename(traits))

        run_build(clear_build, profiling, testing, output, generated_dir, traits, backend)
    except RuntimeError as e:
        print(e)
        sys.exit(1)
    except Exception as e:
        print("ERROR: unexpected error in generator")
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
