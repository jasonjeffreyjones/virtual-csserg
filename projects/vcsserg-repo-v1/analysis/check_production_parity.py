#!/usr/bin/env python3
"""Compare every expected website file with its public production URL."""

from dataclasses import dataclass
import hashlib
from pathlib import Path
import sys
from urllib.parse import quote
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[3]
WEBSITE_ROOT = ROOT / "website"
PRODUCTION_BASE = "https://jasonjones.ninja/virtual-csserg/"
USER_AGENT = "Virtual-CSSERG-parity-check/1.0"


@dataclass(frozen=True)
class Comparison:
    relative_path: str
    status: str
    local_size: int
    remote_size: int | None = None
    detail: str = ""


def compare_site(website_root=WEBSITE_ROOT, base_url=PRODUCTION_BASE, fetch=urlopen):
    """Return byte comparisons for all local files; do not mutate either site."""
    website_root = Path(website_root)
    if not base_url.endswith("/"):
        raise ValueError("base_url must end with /")
    comparisons = []
    for path in sorted(item for item in website_root.rglob("*") if item.is_file()):
        relative = path.relative_to(website_root).as_posix()
        local = path.read_bytes()
        url = base_url + quote(relative, safe="/")
        request = Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with fetch(request, timeout=20) as response:
                remote = response.read()
        except Exception as error:
            comparisons.append(
                Comparison(relative, "unavailable", len(local), detail=str(error))
            )
            continue
        if local == remote:
            comparisons.append(Comparison(relative, "identical", len(local), len(remote)))
        else:
            digest = lambda value: hashlib.sha256(value).hexdigest()[:12]
            comparisons.append(
                Comparison(
                    relative,
                    "different",
                    len(local),
                    len(remote),
                    f"local {digest(local)}; production {digest(remote)}",
                )
            )
    return comparisons


def main():
    comparisons = compare_site()
    counts = {
        status: sum(item.status == status for item in comparisons)
        for status in ("identical", "different", "unavailable")
    }
    print(
        f"Expected {len(comparisons)} files: {counts['identical']} byte-identical, "
        f"{counts['different']} different, {counts['unavailable']} unavailable."
    )
    for item in comparisons:
        if item.status != "identical":
            sizes = f"local={item.local_size}"
            if item.remote_size is not None:
                sizes += f" production={item.remote_size}"
            print(f"[{item.status.upper()}] {item.relative_path}: {sizes}; {item.detail}")
    print(
        "This expected-file probe cannot detect extra stale files in production; "
        "confirm remote inventory separately."
    )
    return 0 if counts["identical"] == len(comparisons) else 1


if __name__ == "__main__":
    sys.exit(main())
