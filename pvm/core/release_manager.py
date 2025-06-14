from collections import defaultdict
from dataclasses import dataclass

from pvm.core.source_manager import SourceManager


@dataclass(frozen=True)
class Release:
    version: str
    date: str
    channel: str


class ReleaseManager:
    def __init__(self, source_manager: SourceManager | None = None):
        self.source_manager = source_manager or SourceManager()

    def find_all_releases(self) -> list[Release]:
        self.source_manager.ensure_src()
        tag_tuples = self.source_manager.get_tag_tuples()
        result = []
        for tag, date in tag_tuples:
            v = tag.replace("php-", "")
            channel = self.detect_channel(v)
            result.append(Release(version=v, date=date, channel=channel))
        return result

    def find_latest_releases(self, major: str = "8") -> dict[str, Release]:
        releases = self.find_all_releases()
        grouped = self._group_by_minor(releases)
        grouped = {k: v for k, v in grouped.items() if k.startswith(f"{major}.")}
        return self._latest_patch_per_minor(grouped)

    @staticmethod
    def detect_channel(version: str) -> str:
        v = version.lower()
        if "rc" in v:
            return "RC"
        if "beta" in v:
            return "Beta"
        if "alpha" in v:
            return "Alpha"
        return "Stable"

    def _group_by_minor(self, releases: list[Release]) -> dict[str, list[Release]]:
        grouped: dict[str, list[Release]] = defaultdict(list)
        for r in releases:
            parts = r.version.split(".")
            if len(parts) < 2 or not all(part.isdigit() for part in parts):
                continue
            major_minor = f"{parts[0]}.{parts[1]}"
            grouped[major_minor].append(r)
        return dict(grouped)

    def _latest_patch_per_minor(self, grouped: dict[str, list[Release]]) -> dict[str, Release]:
        result: dict[str, Release] = {}
        for minor, versions in grouped.items():
            versions_sorted = sorted(versions, key=lambda x: list(map(int, x.version.split("."))), reverse=True)
            result[minor] = versions_sorted[0]
        return result
