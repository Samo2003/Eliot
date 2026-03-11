from __future__ import annotations
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, ClassVar, Type
from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import TemplateError
from eliot.generator.config import GeneratorContext, TEMPLATE_DIR

class GeneratorBase(ABC):
    """
    Abstract base class for all code generation modules.

    Each subclass is automatically registered. Subclasses are responsible 
    for generating specific source files based on the provided `GeneratorContext`.
    """

    # Registry of all generator modules
    registry: ClassVar[List[Type[GeneratorBase]]] = []

    # Shared Jinja2 environment used for template rendering
    env: ClassVar[Environment] = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),      # Initialize template loader
        trim_blocks=True,                           # Strip new lines after generated line
        lstrip_blocks=True                          # Strip white spaces from the beginning of the line
    )

    def __init_subclass__(cls) -> None:
        """
        Automatically instantiate and register each subclass.

        This enables modular extension of the generation pipeline
        without manual registration.
        """

        GeneratorBase.registry.append(cls)

    @abstractmethod
    def generate(self, context: GeneratorContext) -> None:
        """
        Generate files using the provided generation context.
        Must be implemented by each subclass.

        Args:
            context: Provided context for generating
        """
        pass

    def _generate_to_file(
        self, 
        template_name: str, 
        output_path: Path,
        context_data: Dict[str, Any] | None = None
    ) -> None:
        """
        Render a Jinja2 template and write the result to a file.

        Args:
            template_name: Name of template file.
            output_path: Destination path for rendered output.
            context_data: Data passed to the template.
        """

        if context_data is None:
            context_data = {}

        try:
            # Load and render template
            template = self.env.get_template(template_name)
            rendered = template.render(context_data)
        except TemplateError as e:
            # Template syntax or rendering error
            raise RuntimeError(
                f"ERROR: {type(e).__name__} in {template_name}: {e}"
            ) from e
        except Exception as e:
            # Unexpected rendering error
            raise RuntimeError(
                f"ERROR: unexpected error in {template_name}"
            ) from e
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write rendered template to file
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(rendered)
