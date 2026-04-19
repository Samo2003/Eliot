import math
from eliot.generator.config import GeneratorContext
from .base import GeneratorBase

class ValueGeneratorGenerator(GeneratorBase):
    """
    Generator module responsible for producing value generator
    implementations used in the generated C++ code.
    """

    # Number of segments used in Ziggurat algorithm
    N = 128

    def generate(self, context: GeneratorContext) -> None:
        """
        Generate C++ value generator implementations.

        If a normal distribution generator is used, Ziggurat
        lookup tables are generated for efficient sampling.
        """

        # Configure output directory
        generators_dir = context.generated_dir / "generators"

        # If any normal-distribution generator is required,
        # generate Ziggurat lookup tables
        if any(
            "Normal" in generator.type 
            for generator in context.generators
        ):
            template_name = "generators/ZigguratTables.hpp.jinja"
            output_path = generators_dir / "ZigguratTables.hpp"

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

        # Generate individual generator implementations
        for generator in context.generators:
            template_name = f"generators/{generator.type}Generator.hpp.jinja"
            output_name = f"{generator.cpp_type}.hpp"
            output_path = generators_dir / output_name

            self._generate_to_file(
                template_name,
                output_path,
                {
                    "generator": generator
                }
            )

    def _generate_ziggurat_tables(self) -> tuple[list[int], list[float], list[float]]:
        """
        Generate lookup tables for the Ziggurat algorithm
        used for fast normal distribution sampling.

        Based on:
        Marsaglia & Tsang (2000),
        https://www.jstatsoft.org/article/view/v005i08

        Returns:
            kn: Integer cutoff values
            wn: Segment widths
            fn: Function values at segment boundaries
        """

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

        # Compute remaining segments
        for i in range(self.N - 2, 0, -1):
            dn = math.sqrt(-2.0 * math.log(vn / dn + math.exp(-0.5 * dn * dn)))
            kn[i + 1] = int((dn / tn) * m1)
            tn = dn
            fn[i] = math.exp(-0.5 * dn * dn)
            wn[i] = dn / m1

        return kn, wn, fn
