from src.generator.config import GeneratorContext
from .base import GeneratorBase

class PacketGenerator(GeneratorBase):
    def generate(self, context: GeneratorContext) -> None:
        """Generate packet wrapper"""

        # Configure file paths
        template_name = "Packet.hpp.jinja"
        output_path = context.generated_dir / "Packet.hpp"

        self._generate_to_file(
            template_name,
            output_path,
            {
                "traits": context.traits
            }
        )