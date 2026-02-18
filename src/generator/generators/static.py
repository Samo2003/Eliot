import os
import shutil

def generate_static(template_dir: str, output_dir: str, require_calendar: bool) -> None:
    """Copies required static files to output directory"""

    # Configure file path for generating eliot
    src = os.path.join(template_dir, "eliot.cpp")
    dst = os.path.join(output_dir, "eliot.cpp")
    shutil.copy(src, dst)

    static_dir = os.path.join(template_dir, "static")
    dst_dir = os.path.join(output_dir, "static")

    # Create static directory
    os.makedirs(dst_dir, exist_ok=True)

    # Iterate over all items in static directory
    for item in os.listdir(static_dir):
        src = os.path.join(static_dir, item)

        # Ignore calendar dir if it is not required
        if item == "calendar" and not require_calendar:
            continue

        dst = os.path.join(dst_dir, item)

        # Copy source file or dir to destination
        if os.path.isdir(src):
            shutil.copytree(src, dst, dirs_exist_ok=True)
        else:
            shutil.copy(src, dst)