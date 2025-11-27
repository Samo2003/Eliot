from jinja2 import Environment
from ..nf_queue_api import NFQueueApiBase
from ..utils import generate_to_file
import os

def generate_eliot(
    env: Environment, 
    output_dir: str, 
    api: NFQueueApiBase, 
    require_calendar: bool,
    require_time: bool
) -> None:
    """Generate main eliot entry point"""

    # Configure file path
    template_name = "eliot.cpp.jinja"
    output_path = os.path.join(output_dir, "eliot.cpp")

    # Generate file with given context
    generate_to_file(env, template_name, output_path, { "api": api, "require_calendar": require_calendar, "require_time": require_time })
