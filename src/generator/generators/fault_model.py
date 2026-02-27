from src.generator.config import GeneratorContext
from .base import GeneratorBase

class FaultModelGenerator(GeneratorBase):
    def generate(self, context: GeneratorContext) -> None:
        self._generate_header(context)
        self._generate_cpp(context)

    def _generate_header(self, context: GeneratorContext) -> None:
        """Generates fault model header"""
        
        # Configure file paths
        template_name = "FaultModel.hpp.jinja"
        output_path = context.generated_dir / "FaultModel.hpp"

        self._generate_to_file(
            template_name,
            output_path,
            {
                "conditions": context.conditions, 
                "actions": context.actions,
                "states": context.state_nodes,
                "require_calendar": context.require_calendar
            }
        )

    def _generate_cpp(self, context: GeneratorContext) -> None:
        """Generates fault model"""

        # Configure file paths
        template_name = "FaultModel.cpp.jinja"
        output_path = context.generated_dir / "FaultModel.cpp"

        self._generate_to_file(
            template_name,
            output_path,
            {
                "cases": context.cases
            }
        )