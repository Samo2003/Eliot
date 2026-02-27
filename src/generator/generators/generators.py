from typing import List, Tuple
import math
from src.generator.config import GeneratorContext
from .base import GeneratorBase

class ValueGeneratorGenerator(GeneratorBase):
    N = 128

    def generate(self, context: GeneratorContext) -> None:
        # Configure output directory
        generators_dir = context.generated_dir / "generators"

        if any(
            "Normal" in generator.generatorType 
            for generator in context.generators
        ):
            template_name = f"generators/ZigguratTables.hpp.jinja"
            output_name = f"ZigguratTables.hpp"
            output_path = generators_dir / output_name

            kn, wn, fn = self._generate_ziggurat_tables()
            self._generate_to_file(
                template_name,
                output_path,
                {
                    "kn": kn,
                    "wn": wn,
                    "fn": fn
                }
            )

        for generator in context.generators:
            # Configure file path
            template_name = f"generators/{generator.generatorType}Generator.hpp.jinja"
            output_name = f"{generator.cpp_type()}.hpp"
            output_path = generators_dir / output_name

            self._generate_to_file(
                template_name,
                output_path,
                {
                    "generator": generator
                }
            )

    def _generate_ziggurat_tables(self) -> Tuple[List[int], List[float], List[float]]:
        # Source: https://www.jstatsoft.org/article/view/v005i08

        m1 = 2147483648.0
        dn = 3.442619855899
        tn = dn
        vn = 9.91256303526217e-3

        kn = [0] * self.N
        wn = [0.0] * self.N
        fn = [0.0] * self.N

        q = vn / math.exp(-0.5 * dn * dn)

        kn[0] = int((dn / q) * m1)
        kn[1] = 0

        wn[0] = q / m1
        wn[self.N - 1] = dn / m1

        fn[0] = 1.0
        fn[self.N - 1] = math.exp(-0.5 * dn * dn)

        for i in range(self.N - 2, 0, -1):
            dn = math.sqrt(-2.0 * math.log(vn / dn + math.exp(-0.5 * dn * dn)))
            kn[i + 1] = int((dn / tn) * m1)
            tn = dn
            fn[i] = math.exp(-0.5 * dn * dn)
            wn[i] = dn / m1

        return kn, wn, fn
