import sys
import json
from typing import Any, Callable, List
import click
from pathlib import Path
from eliot.generator import Generator, GeneratorConfig
from eliot.DAG import DAG

COMMON_OPTIONS: List[Callable[[Callable[..., Any]], Callable[..., Any]]] = [
    click.option(
        "--dag",
        "-d",
        type=click.Path(exists=True, path_type=Path),
        help="Path to DAG specification file (JSON or YAML)"
    ),
    click.option(
        "--test_case",
        type=click.Path(exists=True, path_type=Path),
        help="Path to test case in file (JSON or YAML)"
    ),
    click.option(
        "--output",
        "-o",
        default=".",
        type=click.Path(path_type=Path, file_okay=False),
        help="Generator output directory"
    ),
]

def apply_common_options(func: Callable[..., Any]) -> Callable[..., Any]:
    for option in reversed(COMMON_OPTIONS):
        func = option(func)
    return func

def execute_generator(
    dag: Path | None,
    test_case: Path | None,
    output: Path, 
    traits: Path, 
    backend: Path, 
    profiling: bool, 
    testing: bool
) -> None:
    """
    Generate pipeline code from DAG specification.
    """

    # Create generator configuration
    config = GeneratorConfig(
        dag_path=dag,
        test_case_path=test_case,
        output_path=output,
        traits_path=traits,
        backend_path=backend,
        profiling=profiling,
        testing=testing
    )

    generator = Generator(config)

    try:
        # Execute generation process
        generator.run()

    except RuntimeError as e:
        # Controlled generator-level error
        click.echo(e, err=True)
        sys.exit(1)

    except Exception as e:
        # Unexpected internal error
        click.echo("ERROR: unexpected error in generator", err=True)
        click.echo(e, err=True)
        sys.exit(1)

@click.group(
    invoke_without_command=True,
    help="Generate packet-processing pipelines from DAG specifications"
)
@click.pass_context
def eliot(ctx: click.Context) -> None:
    if ctx.invoked_subcommand is None:
        ctx.invoke(generate)

@eliot.command(
    help="Generate packet-processing pipelines from DAG specifications"
)
@apply_common_options
@click.option(
    "--traits", 
    "-t",
    required=True,
    type=click.Path(exists=True, path_type=Path), 
    help="Path to traits file linking generated code with backend"
)
@click.option(
    "--backend",
    "-b",
    required=True,
    type=click.Path(exists=True, path_type=Path, file_okay=False),
    help="Path to directory containing CMakeLists.txt"
)
def generate(
    dag: Path | None,
    test_case: Path | None,
    output: Path, 
    traits: Path, 
    backend: Path, 
) -> None:
    execute_generator(
        dag,
        test_case,
        output,
        traits,
        backend,
        profiling=False,
        testing=False
    )

@eliot.command(help="Print DAG JSON schema and exit")
def schema() -> None:
    click.echo(json.dumps(DAG.model_json_schema(), indent=4))
    
@eliot.command(help="Generate code with benchmark backend")
@apply_common_options
def benchmark(dag: Path | None, test_case: Path | None, output: Path) -> None:
    execute_generator(
        dag=dag,
        test_case=test_case,
        output=output,
        traits=Path("traits/BenchmarkTraits.hpp"),
        backend=Path("mocks/benchmark"),
        profiling=False,
        testing=False,
    )
    
@eliot.command(help="Generate code with testing backend")
@apply_common_options
def test(dag: Path | None, test_case: Path | None, output: Path) -> None:
    execute_generator(
        dag=dag,
        test_case=test_case,
        output=output,
        traits=Path("traits/EchoTraits.hpp"),
        backend=Path("mocks/echo"),
        profiling=False,
        testing=True,
    )
    
@eliot.command(help="Generate code with profiling backend")
@apply_common_options
def profile(dag: Path | None, test_case: Path | None, output: Path) -> None:
    execute_generator(
        dag=dag,
        test_case=test_case,
        output=output,
        traits=Path("traits/ProfilingTraits.hpp"),
        backend=Path("mocks/profiling"),
        profiling=True,
        testing=False,
    )

def main() -> None:
    eliot()

if __name__ == "__main__":
    main()
