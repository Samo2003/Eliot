from src.generator.config import GeneratorContext
from .base import GeneratorBase

class PacketProcessorGenerator(GeneratorBase):
    def generate(self, context: GeneratorContext) -> None:
        """Generate packet processor"""
        # Configure file path
        template_name = "PacketProcessor.hpp.jinja"
        output_path = context.generated_dir / "PacketProcessor.hpp"

        self._generate_to_file(
            template_name,
            output_path,
            {
                "require_calendar": context.require_calendar,
                "require_time": context.require_time
            }
        )