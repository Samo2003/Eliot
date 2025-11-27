from jinja2 import Environment
import os
from ..utils import generate_to_file

def generate_time(env: Environment, output_dir: str, require_time: bool) -> None:
    """Generate time module"""

    # Only generate if time is required
    if not require_time:
        return

    # Configure file paths
    template_name = "Time.hpp.jinja"
    output_path = os.path.join(output_dir, "Time.hpp")

    # Generate file with given context
    generate_to_file(env, template_name, output_path)
