from typing import Optional

import typer

from pvm.commands import doctor_command, install_command, releases_command, setup_command, use_command

app = typer.Typer()


@app.command()
def releases() -> None:
    """Show latest PHP releases."""
    releases_command()


@app.command()
def use(version: str) -> None:
    """Prints export statement to use the specified PHP version in the current shell."""
    use_command(version)


@app.command()
def install(
    version: str,
    flags: Optional[list[str]] = typer.Argument(None, help="Build flags to pass to configure"),
    show_flags: bool = typer.Option(False, "--show-flags", help="Show available build flags for this PHP version"),
) -> None:
    """Install a specific PHP version with optional build flags."""
    install_command(version, flags, show_flags)


@app.command()
def setup() -> None:
    """Setup PVM by adding shims to shell configuration."""
    setup_command()


@app.command()
def doctor() -> None:
    """Check for required build dependencies to build PHP(bison, autoconf, re2c...etc)."""
    doctor_command()
