from eliot.generator.config import GeneratorContext
from .base import GeneratorBase

class CMakeGenerator(GeneratorBase):
    """
    Generator module responsible for producing CMakeLists.txt.
    """

    def generate(self, context: GeneratorContext) -> None:
        """
        Generate CMakeLists.txt.
        """
        
        template_name = "CMakeLists.txt.jinja"
        
        output_name = "CMakeLists.txt"
        output_path = context.build.output_dir / output_name
        
        # Render action template
        self._generate_to_file(
            template_name,
            output_path,
            {
                "binary": context.build.binary_name,
                "backend_dir": str(context.build.backend_path),
                "traits_dir": str(context.build.traits_dir),
                "testing": context.build.testing,
                "profiling": context.build.profiling
            }
        )
