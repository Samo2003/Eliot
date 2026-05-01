from eliot.generator.config import GeneratorContext
from .base import GeneratorBase

class PacketGenerator(GeneratorBase):
    """
    Generator module responsible for producing the central
    packet wrapper abstraction.
    """

    def generate(self, context: GeneratorContext) -> None:
        """
        Generate Packet.hpp file.
        """

        # Template defining packet wrapper structure
        template_name = "Packet.hpp.jinja"

        # Output file location
        output_path = context.dag.generated_dir / "Packet.hpp"

        # Render template with traits binding
        self._generate_to_file(
            template_name,
            output_path,
            {
                "traits": context.dag.traits
            }
        )