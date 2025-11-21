from ..DAG import *
from .nf_queue_api import *
from jinja2 import Environment, FileSystemLoader
from .generators import *
from .utils import collect_nodes

def generate(dag: DAG, template_dir: str, output_dir: str, api: NFQueueApiBase) -> None:
    """Main generator function handeling generating"""

    # Collect nodes from DAG that need to be generated
    guard_nodes, action_nodes, generator_nodes = collect_nodes(dag.root)

    # Only generate calendar if at least one action node requires it
    require_calendar = any([action.calendar() for action in action_nodes])

    # Initialize jinja environment
    env = Environment(
        loader=FileSystemLoader(template_dir),  # Initialize template loader
        trim_blocks=True,                       # Strip new lines after generated line
        lstrip_blocks=True                      # Strip white spaces from the beggining of the line
    )

    # Generate neccessary files
    guards.generate_guards(env, output_dir, guard_nodes)
    actions.generate_actions(env, output_dir, action_nodes)
    generators.generate_generators(env, output_dir, generator_nodes)
    packet.generate_packet(env, output_dir, api)
    interfaces.generate_interfaces(env, output_dir)
    processor.generate_processor_header(env, output_dir, api, guard_nodes, action_nodes, require_calendar)
    processor.generate_processor(env, output_dir, dag)
    calendar.generate_calendar(env, output_dir, require_calendar)
    eliot.generate_eliot(env, output_dir, api, require_calendar)
    cmake.generate_cmake(template_dir, output_dir)
