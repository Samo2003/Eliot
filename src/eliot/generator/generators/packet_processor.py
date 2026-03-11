from eliot.generator.config import GeneratorContext
from .base import GeneratorBase

class PacketProcessorGenerator(GeneratorBase):
    """
    Generator module responsible for producing the core packet
    processing component.
    """

    def generate(self, context: GeneratorContext) -> None:
        """
        Generate PacketProcessor.hpp file.

        The template is configured dynamically depending on
        required runtime features extracted from the DAG.
        """

        # Template defining packet processing logic
        template_name = "PacketProcessor.hpp.jinja"

        # Output file path
        output_path = context.generated_dir / "PacketProcessor.hpp"

        # Render template with feature flags derived from DAG analysis
        self._generate_to_file(
            template_name,
            output_path,
            {
                "require_calendar": context.require_calendar,
                "require_time": context.require_time
            }
        )
