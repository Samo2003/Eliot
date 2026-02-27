from src.generator.config import GeneratorContext
from .base import GeneratorBase

class StateGenerator(GeneratorBase):
    def generate(self, context: GeneratorContext) -> None:
        """Generate required state nodes"""

        # Configure output directory
        state_dir = context.generated_dir / "states"

        for state in context.state_nodes:
            # Configure file paths
            template_name = f"states/StateNode.hpp.jinja"
            output_name = f"{state.cpp_type()}.hpp"
            output_path = state_dir / output_name

            self._generate_to_file(
                template_name,
                output_path,
                {
                    "state": state
                }
            )
