from dataclasses import dataclass
from pathlib import Path
from typing import List, Set
from pydantic import BaseModel, model_validator
from src.DAG import Condition, Action, StateNode, ValueGeneratorBase
from .dag_processing.types import Case

# Name of the compiled binary
BINARY_NAME = "eliot"

# Directory containing C++ template files used during generation
TEMPLATE_DIR = "./templates"

class GeneratorConfig(BaseModel):
    """
    Configuration model for the Eliot generator.

    This model represents validated CLI parameters and ensures
    that required combinations of arguments are satisfied.
    """

    source_root: Path
    dag_path: Path | None
    test_case_path: Path | None
    output_path: Path
    traits_path: Path
    backend_path: Path
    profiling: bool
    testing: bool
    print_schema: bool

    @model_validator(mode="after")
    def validate_config(self):
        """
        Ensures that exactly one input source is provided.
        """
        if self.print_schema:
            return self
        
        if (self.dag_path is None) == (self.test_case_path is None):
            raise ValueError("Exactly one input file must be provided (--dag or --test_case)")

        return self

@dataclass
class GeneratorContext:
    """
    Intermediate representation used during code generation.

    This context is produced by `DAGProcessor` and consumed by
    generator modules. It aggregates all semantic elements
    extracted from the DAG.
    """

    # Path to directory where files are generated
    generated_dir: Path

    # Unique conditions
    conditions: Set[Condition]

    # Unique actions
    actions: Set[Action]

    # All state nodes from DAG
    state_nodes: Set[StateNode]

    # Value generators
    generators: Set[ValueGeneratorBase[str, int | float]]

    # Traits file name
    traits: str

    # Flags indicating required code features
    require_calendar: bool
    require_time: bool

    # Processed execution cases
    cases: List[Case]
