from typing import Callable, Optional

from pvm.core.config import PVMConfig


class SourceManager:
    """
    Manages the PHP source tree for PVM. Handles clone, fetch, tag listing, and version checkout.
    """

    def __init__(
        self,
        config: PVMConfig | None = None,
        run_cmd: Optional[Callable] = None,
        check_output: Optional[Callable] = None,
    ):
        self.config = config or PVMConfig()
        import subprocess

        self.run_cmd = run_cmd or subprocess.run
        self.check_output = check_output or subprocess.check_output
        from rich.console import Console

        self.console = Console()

    def ensure_src(self) -> None:
        if not self.config.src_dir.exists():
            self.config.pvm_dir.mkdir(exist_ok=True)
            self.console.print("[yellow]Cloning php-src for the first time. This may take a while...[/yellow]")
            self.run_cmd(
                ["git", "clone", "https://github.com/php/php-src.git", str(self.config.src_dir)],
                check=True,
            )
        self.run_cmd(["git", "fetch", "--tags"], cwd=self.config.src_dir, check=True)

    def get_tags(self) -> list[str]:
        self.ensure_src()
        out = self.check_output(
            [
                "git",
                "for-each-ref",
                "--sort=-creatordate",
                "--format=%(refname:short)",
                "refs/tags/php-*",
            ],
            cwd=self.config.src_dir,
            text=True,
        )
        return [line.strip() for line in out.strip().splitlines() if line.strip()]

    def get_tag_tuples(self) -> list[tuple[str, str]]:
        self.ensure_src()
        out = self.check_output(
            [
                "git",
                "for-each-ref",
                "--sort=-creatordate",
                "--format=%(refname:short) %(creatordate:format:%Y-%m-%d)",
                "refs/tags/php-*",
            ],
            cwd=self.config.src_dir,
            text=True,
        )
        result = []
        for line in out.strip().splitlines():
            if not line.strip():
                continue
            parts = line.strip().split()
            if len(parts) == 2:
                tag, date = parts
                result.append((tag, date))
        return result

    def checkout(self, version: str) -> None:
        tag = f"php-{version}"
        self.run_cmd(["git", "checkout", tag], cwd=self.config.src_dir, check=True)
