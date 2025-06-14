import subprocess
from typing import Optional

from pvm.core.config import PVMConfig
from pvm.core.installer import Installer
from pvm.core.source_manager import SourceManager


def install_command(
    version: str,
    flags: Optional[list[str]] = None,
    show_flags: bool = False,
    config: PVMConfig | None = None,
) -> None:
    config = config or PVMConfig()
    if flags is None:
        flags = []
    if show_flags:
        sm = SourceManager(config=config)
        sm.ensure_src()
        sm.checkout(version)
        src_dir = config.src_dir
        try:
            out = subprocess.check_output(["./configure", "--help"], cwd=src_dir, text=True)  # noqa: S603
            print(out)
        except subprocess.CalledProcessError as e:
            print(f"Error running ./configure --help: {e}")
        return
    # Add double dashes to flags if they don't already have them
    processed_flags = []
    if flags:
        for flag in flags:
            if not flag.startswith("--"):
                processed_flags.append(f"--{flag}")
            else:
                processed_flags.append(flag)
    Installer(config=config).install(version, processed_flags)
    print(f"\nTo use PHP {version} in your current shell, run:")
    print(f'  eval "$(pvm use {version})"')
    print(f"\nTo persist PHP {version} in your shell configuration:")
    print(f"  echo 'eval \"$(pvm use {version})\"'>> ~/.zshrc  # For Zsh users")
    print(f"  echo 'eval \"$(pvm use {version})\"'>> ~/.bashrc  # For Bash users")
