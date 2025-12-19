import pytest
from pathlib import Path
from tests.runner import CaseRunner

@pytest.fixture(scope="session")
def output_dir() -> Path:
    output = Path(__file__).parent / "output"
    output.mkdir(exist_ok=True)
    return output

@pytest.fixture
def case_runner(output_dir: Path) -> CaseRunner:
    return CaseRunner(output_dir)
