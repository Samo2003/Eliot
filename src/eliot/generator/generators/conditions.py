from eliot.generator.config import GeneratorContext
from .base import GeneratorBase

class ConditionGenerator(GeneratorBase):
    """
    Generator module responsible for producing C++ condition
    implementations extracted from the DAG.
    """

    def generate(self, context: GeneratorContext) -> None:
        """
        Generate C++ condition classes.

        For every condition collected in GeneratorContext,
        a corresponding header file is generated in the
        'conditions/' directory.
        """

        # Directory where generated condition headers are stored
        conditions_dir = context.generated_dir / "conditions"
        
        for condition in context.conditions:
            # Template selected based on condition type
            template_name = f"conditions/{condition.conditionType}Condition.hpp.jinja"

            # Output file name derived from C++ type representation
            output_name = f"{condition.cpp_type()}.hpp"
            output_path = conditions_dir / output_name

            # Render condition template
            self._generate_to_file(
                template_name,
                output_path,
                {
                    "condition": condition
                }
            )
