from jinja2 import Environment
from typing import Set
import os
from ...DAG import *
from ..utils import generate_to_file

def generate_actions(env: Environment, output_dir: str, actions: Set[Action]) -> None:
    actions_dir = os.path.join(output_dir, "actions")

    for action in actions:
        if action.is_final():
            continue

        template_name = f"actions/{action.actionType}Action.hpp.jinja"
        output_name = f"{action.cpp_type()}.hpp"
        output_path = os.path.join(actions_dir, output_name)
        generate_to_file(env, template_name, output_path, { "action": action })
