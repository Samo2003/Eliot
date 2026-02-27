from dataclasses import dataclass
from pathlib import Path
from typing import List, Set
from pydantic import BaseModel, model_validator
from src.DAG import Condition, Action, StateNode, ValueGeneratorBase
from .dag_processing.types import Case

BINARY_NAME = "eliot"
TEMPLATE_DIR = "./templates"

class GeneratorConfig(BaseModel):
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
        if self.print_schema:
            return self
        
        if (self.dag_path is None) == (self.test_case_path is None):
            raise ValueError("more than 1 or no input file provided")

        return self

@dataclass
class GeneratorContext:
    generated_dir: Path
    conditions: Set[Condition]
    actions: Set[Action]
    state_nodes: Set[StateNode]
    generators: Set[ValueGeneratorBase[str, int | float]]
    traits: str
    require_calendar: bool
    require_time: bool
    cases: List[Case]
