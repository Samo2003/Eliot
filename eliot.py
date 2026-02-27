import sys
import click
from pathlib import Path
from src.generator import Generator, GeneratorConfig

@click.command()
@click.option("--dag", "-d", type=click.Path(exists=True, path_type=Path), help="Path to DAG JSON file")
@click.option("--test_case", "-t", type=click.Path(exists=True, path_type=Path), help="Path to test case in JSON or YAML file")
@click.option("--output", "-o", default=".", type=click.Path(path_type=Path, file_okay=False), help="Generator output directory")
@click.option("--dag_schema", "-s", is_flag=True, help="Print DAG JSON schema and exit")
@click.option("--traits", type=click.Path(exists=True, path_type=Path), help="Path to trait file for backed")
@click.option("--backend", type=click.Path(exists=True, path_type=Path, file_okay=False), help="Path to directory containing CMakeLists.txt for backend")
@click.option("--profiling", is_flag=True, help="Build generated for profiling")
@click.option("--testing", is_flag=True, help="Build generated for testing")
def main(
    dag: Path | None,
    test_case: Path | None,
    output: Path, 
    dag_schema: bool, 
    traits: Path, 
    backend: Path, 
    profiling: bool, 
    testing: bool
) -> None:
    """Main entry point for generator"""

    config = GeneratorConfig(
        source_root=Path(__file__).resolve().parent,
        dag_path=dag,
        test_case_path=test_case,
        output_path=output,
        traits_path=traits,
        backend_path=backend,
        profiling=profiling,
        testing=testing,
        print_schema=dag_schema
    )

    generator = Generator(config)

    try:
        generator.run()
    except RuntimeError as e:
        print(e)
        sys.exit(1)
    except Exception as e:
        print("ERROR: unexpected error in generator")
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
