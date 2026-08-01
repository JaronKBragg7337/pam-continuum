from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "dashboard"
SITE = ROOT / "site"
DATA = ROOT / "data"


def main() -> None:
    SITE.mkdir(exist_ok=True)
    shutil.copytree(SOURCE, SITE, dirs_exist_ok=True)
    site_data = SITE / "data"
    site_data.mkdir(exist_ok=True)
    for path in DATA.glob("*.json"):
        shutil.copy2(path, site_data / path.name)
    print(f"Built static dashboard in {SITE}")


if __name__ == "__main__":
    main()

