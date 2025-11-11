from jinja2 import Environment
from ..utils import generate_to_file
import os

def generate_calendar(env: Environment, output_dir: str, require_calendar: bool) -> None:
    """Generates calendar if it is required"""

    # Only generate if calendar is required
    if not require_calendar:
        return
    
    # Configure output directory
    calendar_dir = os.path.join(output_dir, "calendar")
    
    # Generate all neccesary calendar files
    names = ["Calendar.cpp", "Calendar.hpp"]
    for name in names:
        # Configure file paths
        template_name = f"calendar/{name}.jinja"
        output_path = os.path.join(calendar_dir, name)

        # Generate file with given context
        generate_to_file(env, template_name, output_path)
