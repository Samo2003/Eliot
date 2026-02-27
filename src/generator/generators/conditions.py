from src.generator.config import GeneratorContext
from .base import GeneratorBase

class ConditionGenerator(GeneratorBase):
    def generate(self, context: GeneratorContext) -> None:
        """Generates required conditions"""
        # Configure output directory
        conditions_dir = context.generated_dir / "conditions"
        
        for condition in context.conditions:
            # Configure file paths
            template_name = f"conditions/{condition.conditionType}Condition.hpp.jinja"
            output_name = f"{condition.cpp_type()}.hpp"
            output_path = conditions_dir / output_name

            self._generate_to_file(
                template_name,
                output_path,
                {
                    "condition": condition
                }
            )