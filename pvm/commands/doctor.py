import re
import subprocess

from pvm.core.config import PVMConfig


def doctor_command(config: PVMConfig | None = None) -> None:
    config = config or PVMConfig()
    checks: list[tuple[str, str, bool, str] | tuple[str, str, bool, str, str]] = []
    try:
        out = subprocess.check_output(["bison", "--version"], text=True)  # noqa: S603, S607
        m = re.search(r"bison \(GNU Bison\) (\d+\.\d+(?:\.\d+)?)", out)
        version = m.group(1) if m else "unknown"

        def ver_tuple(v: str) -> tuple[int, ...]:
            return tuple(map(int, (v.split("."))))

        ok = ver_tuple(version) >= (3, 0, 0) if version != "unknown" else False
        checks.append(("bison", version, ok, "3.0+"))
    except Exception:
        checks.append(("bison", "not found", False, "3.0+"))
    try:
        out = subprocess.check_output(["autoconf", "--version"], text=True)  # noqa: S603, S607
        m = re.search(r"autoconf \(GNU Autoconf\) (\d+\.\d+(?:\.\d+)?)", out)
        version = m.group(1) if m else "unknown"

        def ver_tuple(v: str) -> tuple[int, ...]:
            return tuple(map(int, (v.split("."))))

        ok = ver_tuple(version) >= (2, 68) if version != "unknown" else False
        checks.append(("autoconf", version, ok, "2.68+"))
    except Exception:
        checks.append(("autoconf", "not found", False, "2.68+"))
    try:
        out = subprocess.check_output(["re2c", "--version"], text=True)  # noqa: S603, S607
        m = re.search(r"re2c (\d+\.\d+(?:\.\d+)?)", out)
        version = m.group(1) if m else "unknown"

        def ver_tuple(v: str) -> tuple[int, ...]:
            return tuple(map(int, (v.split("."))))

        ok = ver_tuple(version) >= (1, 0, 3) if version != "unknown" else False
        checks.append(("re2c", version, ok, "1.0.3+ (PHP 8.3+)", "0.13.4+ (PHP 8.2 and earlier)"))
    except Exception:
        checks.append(("re2c", "not found", False, "1.0.3+ (PHP 8.3+)", "0.13.4+ (PHP 8.2 and earlier)"))
    print("\nDependency Check:")
    for entry in checks:
        if len(entry) == 5:  # This is the re2c entry with 5 elements
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
