from jinja2 import Environment
from ..nf_queue_api import NFQueueApiBase
from typing import List, Set
from ...DAG import *
import os
from ..utils import generate_to_file, Case

def generate_fault_model_header(
    env: Environment, 
    output_dir: str, 
    api: NFQueueApiBase, 
    guards: Set[Guard], 
    actions: Set[Action],
    state_nodes: Set[StateNode],
    require_calendar: bool
) -> None:
    """Generates fault model header"""

    # COnfigure file paths
    template_name = "FaultModel.hpp.jinja"
    output_path = os.path.join(output_dir, "FaultModel.hpp")

    # Generate file with given context
    generate_to_file(
        env, template_name, output_path, 
        { 
            "api": api, 
            "guards": guards, 
            "actions": actions,
            "states": state_nodes,
            "require_calendar": require_calendar 
        }
    )

def generate_fault_model(env: Environment, output_dir: str, cases: List[Case]) -> None:
    """Generates fault model"""

    # Configure file paths
    template_name = "FaultModel.cpp.jinja"
    output_path = os.path.join(output_dir, "FaultModel.cpp")

    # Generate file with given context
    generate_to_file(env, template_name, output_path, { "cases": cases })
