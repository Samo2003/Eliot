from jinja2 import Environment
from typing import Set
import os
from ...DAG import *
from ..utils import generate_to_file

def generate_conditions(env: Environment, output_dir: str, conditions: Set[Condition]) -> None:
    """Generate required conditions"""

    # Configure output directory
    conditions_dir = os.path.join(output_dir, "conditions")

    for condition in conditions:
        # Configure file paths
        template_name = f"conditions/{condition.conditionType}Condition.hpp.jinja"
        output_name = f"{condition.cpp_type()}.hpp"
        output_path = os.path.join(conditions_dir, output_name)

        # Generate file with given context
        generate_to_file(env, template_name, output_path, { "condition": condition })
