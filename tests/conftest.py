import pytest
from _pytest.config import Config
from _pytest.config.argparsing import Parser
from pathlib import Path
from tests.runner import CaseRunner

@pytest.fixture(scope="session")
def output_dir() -> Path:
    output = Path(__file__).parent / "output"
    output.mkdir(exist_ok=True)
    return output

def pytest_addoption(parser: Parser):
    parser.addoption(
        "--eliot-debug",
        action="store_true",
        default=False,
        help="Enable debug dump on failure"
    )

@pytest.fixture
def case_runner(output_dir: Path, pytestconfig: Config) -> CaseRunner:
    debug: bool = pytestconfig.getoption("--eliot-debug")
    return CaseRunner(output_dir, debug)
