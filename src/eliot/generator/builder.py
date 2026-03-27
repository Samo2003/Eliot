import shutil
import subprocess
from .config import ROOT_DIR, BINARY_NAME, GeneratorConfig

class Builder:
    """
    Responsible for handling filesystem preparation and invoking
    the CMake-based build process for generated code.
    """

    def __init__(self, config: GeneratorConfig):
        self._cfg = config

        # Directory where generated C++ source files are placed
        self.generated_dir = self._cfg.output_path / "generated"

        # Directory used by CMake for out-of-source build
        self._build_dir = self._cfg.output_path / "build"

    def clear_generated_dir(self) -> None:
        """
        Removes the existing generated directory (if any)
        and recreates it as an empty directory.
        """

        if self.generated_dir.exists():
            shutil.rmtree(self.generated_dir, ignore_errors=True)

        self.generated_dir.mkdir(parents=True, exist_ok=True)

    def build(self) -> None:
        """
        Executes the build pipeline.
        """

        self._build_dir.mkdir(parents=True, exist_ok=True)

        self._configure_cmake()
        self._run_cmake()

    def _configure_cmake(self) -> None:
        """
        Runs CMake configuration step.

        Passes necessary directories and optional flags
        (profiling/testing) as CMake definitions.
        """

        cmake_args = [
            "cmake",
            "-G", "Ninja",
            "-S", str(ROOT_DIR),
            "-B", str(self._build_dir),
            f"-DGENERATED_DIR={self.generated_dir}",
            f"-DTRAITS_DIR={self._cfg.traits_path.parent}",
            f"-DBACKEND_DIR={self._cfg.backend_path.resolve()}",
            f"-DELIOT_BINARY_NAME={BINARY_NAME}"
        ]

        # Enable profiling configuration
        if self._cfg.profiling:
            cmake_args.append("-DPROFILING=ON")

        # Enable testing configuration
        if self._cfg.testing:
            cmake_args.append("-DTESTING=ON")

        # Avoid unnecessary reconfiguration in testing mode
        if not self._cfg.testing or not (self._build_dir / "CMakeCache.txt").exists():
            shutil.rmtree(self._build_dir, ignore_errors=True)
            subprocess.run(cmake_args, check=True)

    def _run_cmake(self) -> None:
        """
        Builds the project using CMake.
        """

        build_args = [
            "cmake",
            "--build", str(self._build_dir)
        ]

        # Enable parallel build for faster compilation
        if not self._cfg.testing:
            build_args.append("--parallel")

        subprocess.run(build_args, check=True)

        # Expected compiled binary path
        binary = self._build_dir / BINARY_NAME

        # Validate successful build
        if not binary.exists():
            raise RuntimeError("ERROR: build failed no binary file found")
        
        target = self._cfg.output_path / BINARY_NAME
        
        # Remove old binary if it exists
        if target.exists():
            target.unlink()
        
        # Copy resulting binary to output directory
        shutil.copy2(binary, target)
