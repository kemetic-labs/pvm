import multiprocessing
import subprocess
from pathlib import Path

from pvm.core.source_manager import SourceManager


class Installer:
    def __init__(self, source_manager: SourceManager | None = None):
        self.source_manager = source_manager or SourceManager()

    def install(self, version: str, flags: list[str]):
        home = Path.home()
        pvm_dir = home / ".pvm"
        src_dir = pvm_dir / "php-src"
        versions_dir = pvm_dir / "versions"
        install_dir = versions_dir / version
        self.source_manager.ensure_src()
        self.source_manager.checkout(version)
        versions_dir.mkdir(exist_ok=True)
        tag = f"php-{version}"
        subprocess.run(["git", "checkout", tag], cwd=src_dir, check=True)  # noqa: S603, S607
        subprocess.run(["./buildconf", "--force"], cwd=src_dir, check=True)  # noqa: S603
        configure = ["./configure", f"--prefix={install_dir}", *flags]
        subprocess.run(configure, cwd=src_dir, check=True)  # noqa: S603
        jobs = str(multiprocessing.cpu_count())
        subprocess.run(["make", f"-j{jobs}"], cwd=src_dir, check=True)  # noqa: S603, S607
        subprocess.run(["make", "install"], cwd=src_dir, check=True)  # noqa: S603, S607
        bin_dir = install_dir / "bin"
        shims_dir = pvm_dir / "shims"
        shims_dir.mkdir(exist_ok=True)
        for binexec in ["php", "phpize", "php-config", "phar", "phpdbg", "php-cgi"]:
            src = bin_dir / binexec
            dst = shims_dir / binexec
            if src.exists():
                if dst.exists():
                    dst.unlink()
                dst.symlink_to(src)
