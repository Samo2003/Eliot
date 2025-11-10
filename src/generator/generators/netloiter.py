from jinja2 import Environment
from ..nf_queue_api import NFQueueApiBase
from ..utils import generate_to_file
import os

def generate_netloiter(
    env: Environment, 
    output_dir: str, 
    api: NFQueueApiBase, 
    require_calendar: bool
) -> None:
    template_name = "netloiter.cpp.jinja"
    output_path = os.path.join(output_dir, "netloiter.cpp")
    generate_to_file(env, template_name, output_path, { "api": api, "require_calendar": require_calendar})
