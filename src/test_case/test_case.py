import yaml
import json
from pathlib import Path
from typing import List, Literal
from pydantic import BaseModel
from src.DAG import Condition, Action

__test__ = False

class Rule(BaseModel):
    """Represent rule in test case"""

    type: Literal["all", "any"]
    conditions: List[Condition]
    actions: List[Action]

class TestCase(BaseModel):
    """Represents test case"""

    defaultAction: Literal["Finish", "Drop"]
    rules: List[Rule]

def load_test_case(file_path: Path) -> TestCase:
    """Load test case from `file_path`, support JSON and YAML format"""

    # Get file extension to determine type
    ext = file_path.suffix.lower()

    with open(file_path, "r", encoding="utf-8") as file:
        if ext == ".yaml":
            data = yaml.safe_load(file)
        elif ext == ".json":
            data = json.load(file)
        else:
            raise ValueError(f"Unsupported file type: {ext}")

    return TestCase.model_validate(data)
