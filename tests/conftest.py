import shutil

import pytest
from _pytest.config import Config
from _pytest.config.argparsing import Parser
from pathlib import Path
from .runner import CaseRunner

OUTPUT_DIR = Path(__file__).parent / "output"

@pytest.fixture(scope="session")
def output_dir() -> Path:
    """
    Provide shared output directory for the entire test session.

    The directory is created once and reused across all test cases.
    """
    OUTPUT_DIR.mkdir(exist_ok=True)
    return OUTPUT_DIR

def pytest_addoption(parser: Parser) -> None:
    """
    Register custom CLI options for pytest.

    --eliot-debug:
        Enables verbose debug output (stdout/stderr dump)
        when test execution fails.
    """

    parser.addoption(
        "--eliot-debug",
        action="store_true",
        default=False,
        help="Enable debug dump on failure"
    )
    
    parser.addoption(
        "--clean",
        action="store_true",
        default=False,
        help="Clean test output directory"
    )
    
def pytest_configure(config: Config) -> None:
    """
    Handle global pytest configuration.
    """

    if config.getoption("--clean"):
        shutil.rmtree(OUTPUT_DIR, ignore_errors=True)

@pytest.fixture
def case_runner(output_dir: Path, pytestconfig: Config) -> CaseRunner:
    """
    Provide configured CaseRunner instance for each test.

    The debug mode is controlled via pytest CLI option.
    """

    debug: bool = pytestconfig.getoption("--eliot-debug")
    return CaseRunner(output_dir, debug)
