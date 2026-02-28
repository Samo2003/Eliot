from src.generator.config import GeneratorContext
from .base import GeneratorBase

class FaultModelGenerator(GeneratorBase):
    """
    Generator module responsible for producing the FaultModel
    implementation.
    """

    def generate(self, context: GeneratorContext) -> None:
        """
        Generate both header and implementation files
        for the fault model.
        """

        self._generate_header(context)
        self._generate_cpp(context)

    def _generate_header(self, context: GeneratorContext) -> None:
        """
        Generate FaultModel.hpp.
        """
        
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
        """
        Generate FaultModel.cpp.
        """

        template_name = "FaultModel.cpp.jinja"
        output_path = context.generated_dir / "FaultModel.cpp"

        self._generate_to_file(
            template_name,
            output_path,
            {
                "cases": context.cases
            }
        )