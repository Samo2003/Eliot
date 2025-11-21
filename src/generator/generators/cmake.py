import os
import shutil

def generate_cmake(template_dir: str, output_dir: str) -> None:
    """Copies template CMakeLists.txt to output directory"""
    src = os.path.join(template_dir, "CMakeLists_template.txt")
    dst = os.path.join(output_dir, "CMakeLists.txt")
    shutil.copyfile(src, dst)
