from jinja2 import Environment
from ..nf_queue_api import NFQueueApiBase
from typing import Set
from ...DAG import *
import os
from ..utils import get_cases, generate_to_file

def generate_processor_header(
    env: Environment, 
    output_dir: str, 
    api: NFQueueApiBase, 
    guards: Set[Guard], 
    actions: Set[Action], 
    require_calendar: bool
) -> None:
    """Generates processor header"""

    # COnfigure file paths
    template_name = "Processor.hpp.jinja"
    output_path = os.path.join(output_dir, "Processor.hpp")

    # Generate file with given context
    generate_to_file(
        env, template_name, output_path, 
        { 
            "api": api, 
            "guards": guards, 
            "actions": [action for action in actions if not action.is_final()],         # Only add non final node incudes
            "require_calendar": require_calendar 
        }
    )

def generate_processor(env: Environment, output_dir: str, dag: DAG) -> None:
    """Generates processor"""

    # Configure file paths
    template_name = "Processor.cpp.jinja"
    output_path = os.path.join(output_dir, "Processor.cpp")

    # Get context list of cases
    cases = get_cases(dag)

    # Generate file with given context
    generate_to_file(env, template_name, output_path, { "cases": cases })
