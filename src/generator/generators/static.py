import shutil
from pathlib import Path
from src.generator.config import TEMPLATE_DIR, GeneratorContext
from .base import GeneratorBase

class StaticGenerator(GeneratorBase):
    """
    Generator module responsible for copying static source files
    and runtime support files into the generated directory.

    These files are not dynamically generated via templates,
    but are required for the final C++ project structure.
    """

    def generate(self, context: GeneratorContext) -> None:
        """
        Copy static template files into the output directory.

        Some subdirectories are included
        conditionally based on the generation context.
        """

        # Copy main entry source file
        shutil.copy2(
            Path(TEMPLATE_DIR) / "eliot.cpp",
            context.generated_dir / "eliot.cpp"
        )

        # Static support directory
        static_dir = Path(TEMPLATE_DIR) / "static"
        dst_dir = context.generated_dir / "static"

        dst_dir.mkdir(parents=True, exist_ok=True)

        # Copy all files and subdirectories from static template directory
        for src in static_dir.iterdir():

            # Conditionally include calendar only if required
            if src.name == "calendar" and not context.require_calendar:
                continue

            dst = dst_dir / src.name

            # Recursively copy directories or copy single files
            if src.is_dir():
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dst)
        