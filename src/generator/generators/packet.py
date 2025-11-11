from jinja2 import Environment
from ..nf_queue_api import NFQueueApiBase
import os
from ..utils import generate_to_file

def generate_packet(env: Environment, output_dir: str, api: NFQueueApiBase) -> None:
    """Generate packet wrapper"""

    # Configure file paths
    template_name = "Packet.hpp.jinja"
    output_path = os.path.join(output_dir, "Packet.hpp")

    # Generate file with given context
    generate_to_file(env, template_name, output_path, { "api": api })
