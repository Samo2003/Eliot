from pathlib import Path
import pytest
from tests.runner import CaseRunner

CASES_DIR = Path(__file__).parent / "cases"

@pytest.mark.parametrize(
    "case_path",
    list(CASES_DIR.rglob("config.yaml")),
    ids=lambda p: str(p.parent.relative_to(CASES_DIR))
)
def test(case_path: Path, case_runner: CaseRunner):
    case_runner.run(case_path)
