import shutil
from pathlib import Path
from src.generator.config import TEMPLATE_DIR, GeneratorContext
from .base import GeneratorBase

class StaticGenerator(GeneratorBase):
    def generate(self, context: GeneratorContext) -> None:
        """Copies required static files to output directory"""

        # Configure file path for generating eliot
        shutil.copy2(
            Path(TEMPLATE_DIR) / "eliot.cpp",
            context.generated_dir / "eliot.cpp"
        )

        static_dir = Path(TEMPLATE_DIR) / "static"
        dst_dir = context.generated_dir / "static"
        dst_dir.mkdir(parents=True, exist_ok=True)

        # Iterate over all items in static directory
        for src in static_dir.iterdir():
            # Ignore calendar dir if it is not required
            if src.name == "calendar" and not context.require_calendar:
                continue

            dst = dst_dir / src.name

            # Copy source file or dir to destination
            if src.is_dir():
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dst)
        