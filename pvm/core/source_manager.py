from pathlib import Path
from typing import Any, Callable, Optional


class SourceManager:
    def __init__(
        self,
        home: Path | None = None,
        run_cmd: Optional[Callable] = None,
        check_output: Optional[Callable] = None,
        console: Any = None,
    ):
        self.home = home or Path.home()
        self.pvm_dir = self.home / ".pvm"
        self.src_dir = self.pvm_dir / "php-src"
        import subprocess

        self.run_cmd = run_cmd or subprocess.run
        self.check_output = check_output or subprocess.check_output
        if console is None:
            from rich.console import Console

            self.console = Console()
        else:
            self.console = console

    def ensure_src(self):
        if not self.src_dir.exists():
            self.pvm_dir.mkdir(exist_ok=True)
            self.console.print("[yellow]Cloning php-src for the first time. This may take a while...[/yellow]")
            self.run_cmd(
                ["git", "clone", "https://github.com/php/php-src.git", str(self.src_dir)],
                check=True,
            )
        self.run_cmd(["git", "fetch", "--tags"], cwd=self.src_dir, check=True)

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
            cwd=self.src_dir,
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
            cwd=self.src_dir,
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

    def checkout(self, version: str):
        tag = f"php-{version}"
        self.run_cmd(["git", "checkout", tag], cwd=self.src_dir, check=True)
