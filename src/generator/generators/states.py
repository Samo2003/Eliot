from jinja2 import Environment
from typing import Set
import os
from ...DAG import *
from ..utils import generate_to_file

def generate_states(env: Environment, output_dir: str, states: Set[StateNode]) -> None:
    """Generate required state nodes"""

    # Configure output directory
    state_dir = os.path.join(output_dir, "states")

    for state in states:
        # Configure file paths
        template_name = f"states/StateNode.hpp.jinja"
        output_name = f"{state.cpp_type()}.hpp"
        output_path = os.path.join(state_dir, output_name)

        # Generate file with given context
        generate_to_file(env, template_name, output_path, { "state": state })
