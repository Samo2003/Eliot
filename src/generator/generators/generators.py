from jinja2 import Environment
from typing import Set
import os
from src.DAG.generators import ValueGeneratorBase
from ...DAG import *
from ..utils import generate_to_file

def generate_generators(env: Environment, output_dir: str, generators: Set[ValueGeneratorBase[str, float | int]]) -> None:
    generators_dir = os.path.join(output_dir, "generators")

    for generator in generators:
        template_name = f"generators/{generator.generatorType}Generator.hpp.jinja"
        output_name = f"{generator.cpp_type()}.hpp"
        output_path = os.path.join(generators_dir, output_name)
        generate_to_file(env, template_name, output_path, { "generator": generator })