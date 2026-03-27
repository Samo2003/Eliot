from eliot.generator.config import GeneratorContext
from .base import GeneratorBase

class StateGenerator(GeneratorBase):
    """
    Generator module responsible for producing C++ header files
    representing individual state machine nodes.

    For each `StateNode` extracted from the DAG, a corresponding
    C++ header file is generated using a Jinja2 template.
    """

    def generate(self, context: GeneratorContext) -> None:
        """
        Generate C++ state node definitions.

        Each state node is rendered into a separate header file
        located in the 'states/' directory of the generated output.
        """

        # Directory where state header files are placed
        state_dir = context.generated_dir / "states"

        for state in context.state_nodes:
            # Shared template used for all state nodes
            template_name = "states/StateNode.hpp.jinja"

            # Output file name derived from state C++ type representation
            output_name = f"{state.cpp_type}.hpp"
            output_path = state_dir / output_name

            # Render template with state-specific data
            self._generate_to_file(
                template_name,
                output_path,
                {
                    "state": state
                }
            )
