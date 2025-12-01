from typing import List, Literal
from pydantic import BaseModel
from ..DAG.guards import Guard
from ..DAG.actions import Action
import os
import yaml
import json

class Rule(BaseModel):
    """Represent rule in test case"""

    type: Literal["all", "any"]
    guards: List[Guard]
    actions: List[Action]

class TestCase(BaseModel):
    """Represents test case"""

    defaultAction: Literal["Finish", "Drop"]
    rules: List[Rule]

def load_test_case(file_path: str) -> TestCase:
    """Load test case from `file_path`, support JSON and YAML format"""

    # Get file extension to determine type
    ext = os.path.splitext(file_path)[1].lower()

    with open(file_path, "r", encoding="utf-8") as file:
        if ext == ".yaml":
            data = yaml.safe_load(file)
        elif ext == ".json":
            data = json.load(file)
        else:
            raise ValueError(f"Unsupported file type: {ext}")

    return TestCase.model_validate(data)
