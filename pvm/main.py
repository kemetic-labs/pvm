import re
import subprocess
from typing import Optional

import typer

from pvm.core.installer import Installer
from pvm.core.source_manager import SourceManager
from pvm.releases import releases as fetch_releases

app = typer.Typer()


@app.command()
def releases():
    """Show latest PHP releases."""
    fetch_releases()


@app.command()
def use(version: str):
    """Prints export statement to use the specified PHP version in the current shell."""
    from pathlib import Path

    home = Path.home()
    pvm_dir = home / ".pvm"
    versions_dir = pvm_dir / "versions"
    install_dir = versions_dir / version
    bin_dir = install_dir / "bin"
    shims_dir = pvm_dir / "shims"
    print(f'export PATH="{shims_dir}:{bin_dir}:$PATH"')


@app.command()
def install(
    version: str,
    flags: Optional[list[str]] = None,
    show_flags: bool = typer.Option(False, "--show-flags", help="Show available build flags for this PHP version"),
):
    """Install a specific PHP version with optional build flags."""
    if flags is None:
        flags = typer.Argument(None)
    if show_flags:
        sm = SourceManager()
        sm.ensure_src()
        sm.checkout(version)
        src_dir = sm.src_dir
        try:
            out = subprocess.check_output(["./configure", "--help"], cwd=src_dir, text=True)  # noqa: S603
            print(out)
        except subprocess.CalledProcessError as e:
            print(f"Error running ./configure --help: {e}")
        return
    Installer().install(version, flags or [])
    print(f"\nTo use PHP {version} in your current shell, run:")
    print(f'  eval "$(pvm use {version})"')


@app.command()
def doctor():
    """Check for required build dependencies (bison, autoconf, re2c)."""
    checks = []
    try:
        out = subprocess.check_output(["bison", "--version"], text=True)  # noqa: S603, S607
        m = re.search(r"bison \(GNU Bison\) (\d+\.\d+(?:\.\d+)?)", out)
        version = m.group(1) if m else "unknown"

        def ver_tuple(v):
            return tuple(map(int, (v.split("."))))

        ok = ver_tuple(version) >= (3, 0, 0) if version != "unknown" else False
        checks.append(("bison", version, ok, "3.0+"))
    except Exception:
        checks.append(("bison", "not found", False, "3.0+"))
    try:
        out = subprocess.check_output(["autoconf", "--version"], text=True)  # noqa: S603, S607
        m = re.search(r"autoconf \(GNU Autoconf\) (\d+\.\d+(?:\.\d+)?)", out)
        version = m.group(1) if m else "unknown"

        def ver_tuple(v):
            return tuple(map(int, (v.split("."))))

        ok = ver_tuple(version) >= (2, 68) if version != "unknown" else False
        checks.append(("autoconf", version, ok, "2.68+"))
    except Exception:
        checks.append(("autoconf", "not found", False, "2.68+"))
    try:
        out = subprocess.check_output(["re2c", "--version"], text=True)  # noqa: S603, S607
        m = re.search(r"re2c (\d+\.\d+(?:\.\d+)?)", out)
        version = m.group(1) if m else "unknown"

        def ver_tuple(v):
            return tuple(map(int, (v.split("."))))

        ok = ver_tuple(version) >= (1, 0, 3) if version != "unknown" else False
        checks.append(("re2c", version, ok, "1.0.3+ (PHP 8.3+)", "0.13.4+ (PHP 8.2 and earlier)"))
    except Exception:
        checks.append(("re2c", "not found", False, "1.0.3+ (PHP 8.3+)", "0.13.4+ (PHP 8.2 and earlier)"))
    print("\nDependency Check:")
    for entry in checks:
        if entry[0] == "re2c":
            name, version, ok, req_83, req_82 = entry
            status = "OK" if ok else "MISSING/OUTDATED"
            print(f"  {name:10} {version:15} {status} (required: {req_83}, {req_82})")
        else:
            name, version, ok, req = entry[:4]
            status = "OK" if ok else "MISSING/OUTDATED"
            print(f"  {name:10} {version:15} {status} (required: {req})")
    if all(entry[2] for entry in checks):
        print("\nAll required dependencies are present.")
    else:
        print("\nSome dependencies are missing or outdated. Please install or upgrade them before building PHP.")
