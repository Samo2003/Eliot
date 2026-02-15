from ..DAG.actions.change_state import ChangeState
from ..DAG import *
from .nf_queue_api import *
from jinja2 import Environment, FileSystemLoader
from .generators import *
from .utils import collect_nodes, process_state_nodes, get_cases

def generate(dag: DAG, template_dir: str, output_dir: str, api: NFQueueApiBase) -> None:
    """Main generator function handling generating"""

    # Collect nodes from DAG that need to be generated
    collected_conditions, collected_actions, state_nodes, collected_generators = collect_nodes(dag.root)

    # Only generate calendar if at least one action requires it
    require_calendar = any([action.calendar() for action in collected_actions])

    # Only include time if at least one node requires it
    require_time = require_calendar or any([action.time() for action in collected_actions]) or any([condition.time() for condition in collected_conditions])

    # Get context list of cases
    cases = get_cases(dag)

    # Verify state nodes, ChangeState actions and attach references for generating
    process_state_nodes(state_nodes, [node for node in collected_actions if isinstance(node, ChangeState)], cases)

    # Initialize jinja environment
    env = Environment(
        loader=FileSystemLoader(template_dir),  # Initialize template loader
        trim_blocks=True,                       # Strip new lines after generated line
        lstrip_blocks=True                      # Strip white spaces from the beginning of the line
    )

    # Generate necessary files
    conditions.generate_conditions(env, output_dir, collected_conditions)
    actions.generate_actions(env, output_dir, collected_actions)
    states.generate_states(env, output_dir, state_nodes)
    generators.generate_generators(env, output_dir, collected_generators)
    packet.generate_packet(env, output_dir, api)
    fault_model.generate_fault_model_header(env, output_dir, api, collected_conditions, collected_actions, state_nodes, require_calendar)
    fault_model.generate_fault_model(env, output_dir, cases)
    eliot.generate_eliot(env, output_dir, api, require_calendar, require_time)
    static.generate_static(template_dir, output_dir, require_calendar)
