from pathlib import Path
import pytest
from .runner import CaseRunner

# Directory containing all test case folders
CASES_DIR = Path(__file__).parent / "cases"

@pytest.mark.parametrize(
    "case_path",
    # Recursively find all config.yaml files inside CASES_DIR
    list(CASES_DIR.rglob("config.yaml")),
    ids=lambda p: str(p.parent.relative_to(CASES_DIR))
)
def test(case_path: Path, case_runner: CaseRunner):
    """
    Execute a single test case based on its config.yaml definition.

    Each config.yaml represents one independent test scenario.
    The CaseRunner handles building, executing, and validating the case.
    """
    case_runner.run(case_path)
