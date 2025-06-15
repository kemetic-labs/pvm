from pvm.core.config import PVMConfig


def use_command(version: str, config: PVMConfig | None = None) -> None:
    config = config or PVMConfig()
    install_dir = config.versions_dir / version
    bin_dir = install_dir / "bin"
    shims_dir = config.shims_dir

    shims_dir.mkdir(exist_ok=True)
    for executable_name in ["php", "phpize", "php-config", "phar", "phpdbg", "php-cgi"]:
        src = bin_dir / executable_name
        dst = shims_dir / executable_name
        if src.exists():
            if dst.exists():
                dst.unlink()
            dst.symlink_to(src)

    print(f'shims now point to PHP {version}')
