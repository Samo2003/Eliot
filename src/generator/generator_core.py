from ..DAG.actions.change_state import ChangeState
from ..DAG import *
from .nf_queue_api import *
from jinja2 import Environment, FileSystemLoader
from .generators import *
from .utils import collect_nodes, process_state_nodes, get_cases

def generate(dag: DAG, template_dir: str, output_dir: str, api: NFQueueApiBase) -> None:
    """Main generator function handling generating"""

    # Collect nodes from DAG that need to be generated
    guard_nodes, action_nodes, state_nodes, generator_nodes = collect_nodes(dag.root)

    # Only generate calendar if at least one action node requires it
    require_calendar = any([action.calendar() for action in action_nodes])

    # Only include time if at least one node requires it
    require_time = require_calendar or any([action.time() for action in action_nodes]) or any([guard.time() for guard in guard_nodes])

    # Get context list of cases
    cases = get_cases(dag)

    # Verify state nodes, ChangeState actions and attach references for generating
    process_state_nodes(state_nodes, [node for node in action_nodes if isinstance(node, ChangeState)], cases)

    # Initialize jinja environment
    env = Environment(
        loader=FileSystemLoader(template_dir),  # Initialize template loader
        trim_blocks=True,                       # Strip new lines after generated line
        lstrip_blocks=True                      # Strip white spaces from the beginning of the line
    )

    # Generate necessary files
    guards.generate_guards(env, output_dir, guard_nodes)
    actions.generate_actions(env, output_dir, action_nodes)
    states.generate_states(env, output_dir, state_nodes)
    generators.generate_generators(env, output_dir, generator_nodes)
    packet.generate_packet(env, output_dir, api)
    processor.generate_processor_header(env, output_dir, api, guard_nodes, action_nodes, state_nodes, require_calendar)
    processor.generate_processor(env, output_dir, cases)
    eliot.generate_eliot(env, output_dir, api, require_calendar, require_time)
    static.generate_static(template_dir, output_dir, require_calendar)
