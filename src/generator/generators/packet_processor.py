from jinja2 import Environment
from ..utils import generate_to_file
import os

def generate_packet_processor(
    env: Environment, 
    output_dir: str, 
    require_calendar: bool,
    require_time: bool
) -> None:
    """Generate packet processor"""

    # Configure file path
    template_name = "PacketProcessor.hpp.jinja"
    output_path = os.path.join(output_dir, "PacketProcessor.hpp")

    # Generate file with given context
    generate_to_file(env, template_name, output_path, { "require_calendar": require_calendar, "require_time": require_time })
