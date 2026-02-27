from src.generator.config import GeneratorContext
from .base import GeneratorBase

class ActionGenerator(GeneratorBase):
    def generate(self, context: GeneratorContext) -> None:
        """Generates required actions"""

        actions_dir = context.generated_dir / "actions"
        for action in context.actions:
            # Configure file paths
            template_name = f"actions/{action.actionType}Action.hpp.jinja"
            output_name = f"{action.cpp_type()}.hpp"
            output_path = actions_dir / output_name

            self._generate_to_file(
                template_name,
                output_path,
                {
                    "action": action
                }
            )
