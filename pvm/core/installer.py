import multiprocessing
import subprocess

from pvm.core.config import PVMConfig
from pvm.core.source_manager import SourceManager


class Installer:
    def __init__(self, source_manager: SourceManager | None = None, config: PVMConfig | None = None):
        self.source_manager = source_manager or SourceManager()
        self.config = config or PVMConfig()

    def install(self, version: str, flags: list[str]) -> None:
        src_dir = self.config.src_dir
        versions_dir = self.config.versions_dir
        install_dir = versions_dir / version
        self.source_manager.ensure_src()
        self.source_manager.checkout(version)
        versions_dir.mkdir(exist_ok=True)
        tag = f"php-{version}"
        subprocess.run(["git", "checkout", tag], cwd=src_dir, check=True)  # noqa: S603, S607
        subprocess.run(["./buildconf", "--force"], cwd=src_dir, check=True)  # noqa: S603
        print("[pvm] Running 'make clean' before build...")
        subprocess.run(["make", "clean"], cwd=src_dir, check=True)  # noqa: S603, S607
        configure = ["./configure", f"--prefix={install_dir}", *flags]
        subprocess.run(configure, cwd=src_dir, check=True)  # noqa: S603
        jobs = str(multiprocessing.cpu_count())
        subprocess.run(["make", f"-j{jobs}"], cwd=src_dir, check=True)  # noqa: S603, S607
        subprocess.run(["make", "install"], cwd=src_dir, check=True)  # noqa: S603, S607
        bin_dir = install_dir / "bin"
        shims_dir = self.config.shims_dir
        shims_dir.mkdir(exist_ok=True)
        for executable_name in ["php", "phpize", "php-config", "phar", "phpdbg", "php-cgi"]:
            src = bin_dir / executable_name
            dst = shims_dir / executable_name
            if src.exists():
                if dst.exists():
                    dst.unlink()
                dst.symlink_to(src)
