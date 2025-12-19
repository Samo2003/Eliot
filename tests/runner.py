import os
import yaml
import sys
from pathlib import Path
import socket
import subprocess
import time
from typing import Any, Callable, Dict, List, Tuple, cast
from tests.comm import ReceivedPacket, SentPacket, receive_packets, send_packets
from tests.loader import Case, load_case
from tests.stats import ExchangeStats

BINARY_NAME = "eliot"
BUFFER_SIZE = 4 * 1024 * 1024
AssertFn = Callable[[ExchangeStats], None]

class CaseRunner:
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.workspace: Path

    def run(self, case_path: Path):
        case = load_case(case_path)

        self.workspace = self._workspace(case_path)
        
        binary = self._generate_and_build(case)

        proc = self._run_binary(binary)
        try:
            port = self._read_listen_port(proc)
            sent, received = self._send_packets(case, port)
            stats = ExchangeStats(sent, received)
            self._assert(case_path, stats)
        finally:
            self._stop_binary(proc)

    def _workspace(self, case_path: Path) -> Path:
        cases_root = (Path(__file__).resolve().parent / "cases").resolve()
        rel = case_path.parent.resolve().relative_to(cases_root)
        workspace = self.output_dir / rel
        workspace.mkdir(parents=True, exist_ok=True)
        return workspace
    
    def _write_test_case(self, case: Case) -> Path:
        path = self.workspace / "test_case.yaml"
        with open(path, "w") as f:
            yaml.safe_dump(case.build.model_dump(), f)
        return path
    
    def _generate_and_build(self, case: Case) -> str:
        test_case_path = self._write_test_case(case)
        generator_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        workspace_rel = os.path.relpath(self.workspace, generator_root)

        generator_args = [
            sys.executable,
            "generator.py",
            "-t", str(test_case_path),
            "-o", str(workspace_rel),
            "-a", "echo"
        ]

        generator = subprocess.run(generator_args, cwd=generator_root, text=True, capture_output=True)

        assert generator.returncode == 0, (
            f"stdout:\n{generator.stdout}\n"
            f"stderr:\n{generator.stderr}"
        )
        binary = os.path.join(self.workspace, BINARY_NAME)
        assert os.path.exists(binary)
        return binary

    def _run_binary(self, binary: str) -> subprocess.Popen[str]:
        proc = subprocess.Popen(
            [binary],
            cwd=self.workspace,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        time.sleep(0.2)

        return proc
    
    def _read_listen_port(self, proc: subprocess.Popen[str]) -> int:
        assert proc.stdout is not None
        line = proc.stdout.readline().strip()
        assert line.startswith("LISTEN_PORT=")
        return int(line.split("=")[1])

    def _send_packets(self, case: Case, port: int) -> Tuple[List[SentPacket], List[ReceivedPacket]]:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, BUFFER_SIZE)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFFER_SIZE)
            sock.connect(("127.0.0.1", port))

            sent = send_packets(case.send, sock)
            received = receive_packets(sock, case.timeout)
            
        return sent, received
 
    def _assert(self, case_path: Path, stats: ExchangeStats):
        assert_file = case_path.parent / "assert.py"

        if not assert_file.exists():
            raise RuntimeError(f"Missing assert.py in {case_path.parent}")

        namespace: Dict[str, Any] = {}
        exec(assert_file.read_text(), namespace)

        if "check" not in namespace:
            raise RuntimeError("assert.py must define check(sent: List[SentPacket], received: List[ReceivedPacket])")

        check = cast(AssertFn, namespace["check"])
        check(stats)

    def _stop_binary(self, proc: subprocess.Popen[str]):
        proc.terminate()
        try:
            proc.wait(timeout=1)
        except subprocess.TimeoutExpired:
            proc.kill()
