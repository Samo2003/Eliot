from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from pydantic import BaseModel, model_validator
from importlib.resources import files
from eliot.DAG import Condition, Action, StateNode, ValueGenerator
from .dag_processing.types import Case

# Name of the compiled binary
BINARY_NAME = "eliot-run"

# Projects root directory
# ROOT_DIR = Path(__file__).resolve().parents[3]
ROOT_DIR = files("eliot")

# Directory containing C++ template files used during generation
TEMPLATE_DIR = ROOT_DIR / "templates"

class GeneratorConfig(BaseModel):
    """
    Configuration model for the Eliot generator.

    This model represents validated CLI parameters and ensures
    that required combinations of arguments are satisfied.
    """

    dag_path: Path | None
    test_case_path: Path | None
    output_path: Path
    traits_path: Path
    backend_path: Path
    profiling: bool
    testing: bool

    @model_validator(mode="after")
    def validate_config(self) -> GeneratorConfig:
        """
        Ensures that exactly one input source is provided.
        """        
        if (self.dag_path is None) == (self.test_case_path is None):
            raise ValueError("Exactly one input file must be provided (--dag or --test_case)")

        return self

@dataclass
class DAGContext:
    """
    Intermediate representation used during code generation.

    This context is produced by `DAGProcessor` and consumed by
    generator modules. It aggregates all semantic elements
    extracted from the DAG.
    """

    # Path to directory where files are generated
    generated_dir: Path

    # Unique conditions
    conditions: set[Condition]

    # Unique actions
    actions: set[Action]

    # All state nodes from DAG
    state_nodes: set[StateNode]

    # Value generators
    generators: set[ValueGenerator]

    # Traits file name
    traits: str

    # Flags indicating required code features
    require_calendar: bool
    require_time: bool

    # Processed execution cases
    cases: list[Case]
    
@dataclass
class BuildConfig:
    output_dir: Path
    backend_path: Path
    traits_dir: Path
    binary_name: str
    profiling: bool
    testing: bool
    
@dataclass
class GeneratorContext:
    dag: DAGContext
    build: BuildConfig
