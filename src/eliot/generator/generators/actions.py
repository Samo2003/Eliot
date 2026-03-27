from eliot.generator.config import GeneratorContext
from .base import GeneratorBase

class ActionGenerator(GeneratorBase):
    """
    Generator module responsible for producing C++ action
    implementations extracted from the DAG.
    """

    def generate(self, context: GeneratorContext) -> None:
        """
        Generate C++ action classes.

        For every action collected in GeneratorContext,
        a corresponding header file is generated in the
        'actions/' directory.
        """

        # Directory where generated action headers are stored
        actions_dir = context.generated_dir / "actions"

        for action in context.actions:
            # Template selected based on action type
            template_name = f"actions/{action.actionType}Action.hpp.jinja"

            # Output file name derived from C++ type representation
            output_name = f"{action.cpp_type}.hpp"
            output_path = actions_dir / output_name

            # Render action template
            self._generate_to_file(
                template_name,
                output_path,
                {
                    "action": action
                }
            )
