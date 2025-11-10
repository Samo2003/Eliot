from jinja2 import Environment
from ..utils import generate_to_file
import os

def generate_calendar(env: Environment, output_dir: str, require_calendar: bool) -> None:
    if not require_calendar:
        return
    calendar_dir = os.path.join(output_dir, "calendar")
    
    names = ["Calendar.cpp", "Calendar.hpp"]
    for name in names:
        template_name = f"calendar/{name}.jinja"
        output_path = os.path.join(calendar_dir, name)
        generate_to_file(env, template_name, output_path)
