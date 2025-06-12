from rich.console import Console
from rich.table import Table

from pvm.core.release_service import ReleaseManager


def releases():
    manager = ReleaseManager()
    latest_releases = manager.find_latest_releases("8")
    table = Table(title="Versions")
    table.add_column("Minor", style="cyan", no_wrap=True)
    table.add_column("Version", style="cyan", no_wrap=True)
    table.add_column("Date", style="green")
    table.add_column("Channel", style="magenta")
    for minor in sorted(latest_releases.keys(), key=lambda x: list(map(int, x.split("."))), reverse=True):
        v = latest_releases[minor]
        table.add_row(minor, v.version, v.date, v.channel)
    Console().print(table)
