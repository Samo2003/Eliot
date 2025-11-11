from jinja2 import Environment
import os
from ..utils import generate_to_file

def generate_interfaces(env: Environment, output_dir: str) -> None:
    """Generate interfaces to use zero cost interfaces in C++ code"""

    # Configure output directory
    interface_dir = os.path.join(output_dir, "interfaces")

    # Generate all necessary interfaces
    interfaces = ["Action", "Guard", "GeneratorFloat", "GeneratorInt"]
    for interface in interfaces:
        # Configure file paths
        template_name = f"interfaces/{interface}.hpp.jinja"
        output_name = f"{interface}.hpp"
        output_path = os.path.join(interface_dir, output_name)

        # Generate file with given context
        generate_to_file(env, template_name, output_path)
