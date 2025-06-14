from pvm.core.config import PVMConfig


def use_command(version: str, config: PVMConfig | None = None) -> None:
    config = config or PVMConfig()
    install_dir = config.versions_dir / version
    bin_dir = install_dir / "bin"
    shims_dir = config.shims_dir
    print(f'export PATH="{shims_dir}:{bin_dir}:$PATH"')
