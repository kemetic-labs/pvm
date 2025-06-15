import os
from pathlib import Path

from pvm.core.config import PVMConfig


def setup_command(config: PVMConfig | None = None) -> None:
    """Setup PVM by adding shims to shell configuration."""
    config = config or PVMConfig()
    shims_dir = config.shims_dir

    if not shims_dir.exists() or not any(shims_dir.iterdir()):
        print("Error: No PHP versions installed.")
        print("Please install a PHP version first using: pvm install <version>")
        return

    php_shim = shims_dir / "php"
    if not php_shim.exists():
        print("Error: No PHP shim found.")
        print("Please install a PHP version first using: pvm install <version>")
        return

    home = Path.home()
    shell_configs = [
        (home / ".zshrc", "Zsh"),
        (home / ".bashrc", "Bash"),
    ]

    pvm_export_line = f'export PATH="{shims_dir}:$PATH"'
    pvm_comment = "# Added by PVM"

    updated_configs = []
    already_configured = []
    existing_configs = []

    for config_file, shell_name in shell_configs:
        if config_file.exists():
            existing_configs.append((config_file, shell_name))
            content = config_file.read_text()

            if pvm_export_line in content:
                already_configured.append((config_file, shell_name))
                print(f"{shell_name} configuration ({config_file}) already contains PVM setup.")
                continue

            with config_file.open("a") as f:
                f.write(f"\n{pvm_comment}\n{pvm_export_line}\n")

            updated_configs.append((config_file, shell_name))
            print(f"Added PVM to {shell_name} configuration ({config_file}).")

    if updated_configs:
        print("\nPVM setup complete! To use PVM in your current shell, run:")
        for config_file, shell_name in updated_configs:
            print(f"  source {config_file}  # For {shell_name} users")
        print("\nOr restart your terminal.")
    elif already_configured:
        print("\nPVM is already configured in your shell. No changes needed.")
    elif not existing_configs:
        print("No shell configuration files found (.zshrc or .bashrc).")
        print("You may need to manually add the following to your shell configuration:")
        print(f"  {pvm_export_line}")
    else:
        print("Unexpected configuration state. You may need to manually add:")
        print(f"  {pvm_export_line}")
