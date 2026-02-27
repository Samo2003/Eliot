import shutil
import subprocess
from .config import GeneratorConfig, BINARY_NAME

class Builder():
    def __init__(self, config: GeneratorConfig):
        self._cfg = config
        self.generated_dir = self._cfg.output_path / "generated"
        self._build_dir = self._cfg.output_path / "build"

    def clear_generated_dir(self) -> None:
        """Clears the provided repository if it exists and ensures it is created"""
        if self.generated_dir.exists():
            shutil.rmtree(self.generated_dir, ignore_errors=True)
        self.generated_dir.mkdir(parents=True, exist_ok=True)

    def build(self) -> None:
        self._build_dir.mkdir(parents=True, exist_ok=True)
        self._configure_cmake()
        self._run_cmake()

    def _configure_cmake(self) -> None:
        cmake_args = [
            "cmake",
            "-G", "Ninja",
            "-S", str(self._cfg.source_root),
            "-B", str(self._build_dir),
            f"-DGENERATED_DIR={self.generated_dir}",
            f"-DTRAITS_DIR={self._cfg.traits_path.parent}",
            f"-DBACKEND_DIR={self._cfg.backend_path.resolve()}"
        ]

        if self._cfg.profiling:
            cmake_args.append("-DPROFILING=ON")

        if self._cfg.testing:
            cmake_args.append("-DTESTING=ON")

        if not self._cfg.testing or not (self._build_dir / "CMakeCache.txt").exists():
            subprocess.run(cmake_args, check=True)

    def _run_cmake(self) -> None:
        build_args = [
            "cmake",
            "--build", str(self._build_dir)
        ]

        if not self._cfg.testing:
            build_args.append("--parallel")

        subprocess.run(build_args, check=True)

        binary = self._build_dir / BINARY_NAME

        if not binary.exists():
            raise RuntimeError("ERROR: build failed no binary file found")
        
        shutil.copy2(binary, self._cfg.output_path)
