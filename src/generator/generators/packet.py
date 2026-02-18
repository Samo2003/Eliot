from jinja2 import Environment
import os
from ..utils import generate_to_file

def generate_packet(env: Environment, output_dir: str, traits: str) -> None:
    """Generate packet wrapper"""

    # Configure file paths
    template_name = "Packet.hpp.jinja"
    output_path = os.path.join(output_dir, "Packet.hpp")

    # Generate file with given context
    generate_to_file(env, template_name, output_path, { "traits": traits })
