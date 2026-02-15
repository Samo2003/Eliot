from jinja2 import Environment
from typing import Set
import os
from ...DAG import *
from ..utils import generate_to_file, generate_ziggurat_tables

def generate_generators(env: Environment, output_dir: str, generators: Set[ValueGeneratorBase[str, float | int]]) -> None:
    """Generates required generators"""

    # Configure output directory
    generators_dir = os.path.join(output_dir, "generators")

    if any("Normal" in generator.generatorType for generator in generators):
        template_name = f"generators/ZigguratTables.hpp.jinja"
        output_name = f"ZigguratTables.hpp"
        output_path = os.path.join(generators_dir, output_name)

        kn, wn, fn = generate_ziggurat_tables()

        generate_to_file(env, template_name, output_path, { "kn": kn, "wn": wn, "fn": fn})

    for generator in generators:
        # Configure file path
        template_name = f"generators/{generator.generatorType}Generator.hpp.jinja"
        output_name = f"{generator.cpp_type()}.hpp"
        output_path = os.path.join(generators_dir, output_name)

        # Generate file with given context
        generate_to_file(env, template_name, output_path, { "generator": generator })