from pathlib import Path

from pydantic_settings import BaseSettings


class PVMConfig(BaseSettings):
    home: Path = Path.home()
    pvm_dir: Path = home / ".pvm"
    src_dir: Path = pvm_dir / "php-src"
    versions_dir: Path = pvm_dir / "versions"
    shims_dir: Path = pvm_dir / "shims"

    class Config:
        env_prefix = "PVM_"
        arbitrary_types_allowed = True
