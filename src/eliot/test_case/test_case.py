import yaml
from pathlib import Path
from typing import Literal
from pydantic import BaseModel
from eliot.DAG import Condition, Action

# Prevent pytest from treating this module as a test file
__test__ = False

class Rule(BaseModel):
    """
    Represents a single rule in a test case specification.
    """

    type: Literal["all", "any"]                     # Logical operator defining how conditions are evaluated.
    conditions: list[Condition]                     # List of Conditions.
    actions: list[Action]                           # List of Actions

class TestCase(BaseModel):
    """
    Represents a test case specification.

    This structure serves as an alternative input format
    that can be translated into a DAG representation.
    """

    defaultAction: Literal["Finish", "Drop"]        # Default action applied to packets
    rules: list[Rule]                               # List of rules for evaluation

def load_test_case(file_path: Path) -> TestCase:
    """
    Load and validate a test case specification from a file.

    The file content is validated against the TestCase model.

    Args:
        file_path: Path to file containing TestCase
    
    Returns:
        Validated TestCase object
    """

    with open(file_path, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    return TestCase.model_validate(data)
