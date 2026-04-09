import yaml
import socket
import subprocess
import time
from pathlib import Path
from typing import Any, Callable, cast
from eliot.generator.config import BINARY_NAME, ROOT_DIR
from eliot.test_case.test_case import TestCase
from .comm import ReceivedPacket, SentPacket, receive_packets, send_packets
from .loader import Case, load_case
from .stats import ExchangeStats

BUFFER_SIZE = 4 * 1024 * 1024
AssertFn = Callable[[ExchangeStats], None]

class CaseRunner:
    """
    Responsible for executing a single test case end-to-end.
    """

    def __init__(self, output_dir: Path, debug: bool):
        self.output_dir = output_dir
        self.debug = debug
        self.workspace: Path

    def run(self, case_path: Path) -> None:
        """
        Execute one test case defined by config.yaml.
        """

        case = load_case(case_path)

        self.workspace = self._workspace(case_path)
        
        binary = self._generate_and_build(case)

        proc = self._run_binary(binary)
        try:
            port = self._read_listen_port(proc)
            sent, received = self._send_packets(case, port)
            stats = ExchangeStats(sent, received)
            self._assert(case_path, stats)
        except Exception:
            if self.debug:
                if proc.poll() is None:
                    self._stop_binary(proc)
                self._dump_output(proc)
            raise
        finally:
            if proc.poll() is None:
                self._stop_binary(proc)

    def _workspace(self, case_path: Path) -> Path:
        """
        Create isolated workspace directory for given test case.
        """

        cases_root = (Path(__file__).resolve().parent / "cases").resolve()
        rel = case_path.parent.resolve().relative_to(cases_root)
        workspace = self.output_dir / rel
        workspace.mkdir(parents=True, exist_ok=True)
        return workspace
    
    def _write_test_case(self, case: Case) -> list[str]:
        """
        Serialize test case configuration for generator.
        """

        if isinstance(case.build, TestCase):
            path = self.workspace / "test_case.yaml"
            with open(path, "w", encoding="utf-8") as f:
                yaml.safe_dump(case.build.model_dump(), f)
            return ["--test_case", str(path)]
        else:
            path = self.workspace / "dag.yaml"
            with open(path, "w", encoding="utf-8") as f:
                yaml.safe_dump(case.build.model_dump(), f)
            return ["-d", str(path)]
    
    def _generate_and_build(self, case: Case) -> Path:
        """
        Run generator and build resulting binary.
        """

        build_args = self._write_test_case(case)
        workspace_rel = self.workspace.relative_to(ROOT_DIR)

        generator_args = [
            "eliot", "test",
            *build_args,
            "-o", str(workspace_rel)
        ]

        generator = subprocess.run(generator_args, cwd=ROOT_DIR, text=True, capture_output=True)

        assert generator.returncode == 0, (
            f"stdout:\n{generator.stdout}\n"
            f"stderr:\n{generator.stderr}"
        )

        binary = self.workspace / BINARY_NAME
        assert binary.exists()
        return binary

    def _run_binary(self, binary: Path) -> subprocess.Popen[str]:
        """
        Launch compiled binary in workspace.
        """

        proc = subprocess.Popen(
            [binary],
            cwd=self.workspace,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Give binary time to initialize and print listen port
        time.sleep(0.2)

        return proc
    
    def _read_listen_port(self, proc: subprocess.Popen[str]) -> int:
        """
        Read LISTEN_PORT from binary stdout.
        """
    
        assert proc.stdout is not None
        line = proc.stdout.readline().strip()
        assert line.startswith("LISTEN_PORT=")
        return int(line.split("=")[1])

    def _send_packets(self, case: Case, port: int) -> tuple[list[SentPacket], list[ReceivedPacket]]:
        """
        Send packets to running binary and collect responses.
        """

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, BUFFER_SIZE)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFFER_SIZE)
            sock.connect(("127.0.0.1", port))

            sent = send_packets(case.send, sock)
            received = receive_packets(sock, case.timeout)
            
        return sent, received
 
    def _assert(self, case_path: Path, stats: ExchangeStats) -> None:
        """
        Execute custom assertion logic defined in assert.py.
        """

        assert_file = case_path.parent / "assert.py"

        if not assert_file.exists():
            raise RuntimeError(f"Missing assert.py in {case_path.parent}")

        namespace: dict[str, Any] = {}
        exec(assert_file.read_text(), namespace)

        if "check" not in namespace:
            raise RuntimeError(
                "assert.py must define check(stats: ExchangeStats)"
            )

        check = cast(AssertFn, namespace["check"])
        check(stats)

    def _dump_output(self, proc: subprocess.Popen[str]) -> None:
        try:
            out, err = proc.communicate(timeout=1)

            print("\n====== STDOUT ======")
            print(out)

            print("\n====== STDERR ======")
            print(err)

            print("\n====================\n")

        except Exception as e:
            print(f"Failed to dump process output: {e}")

    def _stop_binary(self, proc: subprocess.Popen[str]) -> None:
        """
        Gracefully terminate binary process.
        """

        proc.terminate()
        try:
            proc.wait(timeout=1)
        except subprocess.TimeoutExpired:
            proc.kill()
