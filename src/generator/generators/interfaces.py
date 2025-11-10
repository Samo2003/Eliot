from jinja2 import Environment
import os
from ..utils import generate_to_file

def generate_interfaces(env: Environment, output_dir: str) -> None:
    interface_dir = os.path.join(output_dir, "interfaces")

    interfaces = ["Action", "Guard", "GeneratorFloat", "GeneratorInt"]
    for interface in interfaces:
        template_name = f"interfaces/{interface}.hpp.jinja"
        output_name = f"{interface}.hpp"
        output_path = os.path.join(interface_dir, output_name)
        generate_to_file(env, template_name, output_path)
