from jinja2 import Environment
from typing import Set
import os
from ...DAG import *
from ..utils import generate_to_file

def generate_guards(env: Environment, output_dir: str, guards: Set[Guard]) -> None:
    """Generate required guards"""

    # Configure output directory
    guards_dir = os.path.join(output_dir, "guards")

    for guard in guards:
        # Configure file paths
        template_name = f"guards/{guard.guardType}Guard.hpp.jinja"
        output_name = f"{guard.cpp_type()}.hpp"
        output_path = os.path.join(guards_dir, output_name)

        # Generate file with given context
        generate_to_file(env, template_name, output_path, { "guard": guard })
