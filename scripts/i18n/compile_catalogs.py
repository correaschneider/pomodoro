from __future__ import annotations

from pathlib import Path

import polib


ROOT = Path(__file__).resolve().parents[2]
LOCALES_DIR = ROOT / "resources" / "locales"
DOMAIN = "pomodoro_app"


def compile_locale(locale_dir: Path) -> None:
    po_path = locale_dir / "LC_MESSAGES" / f"{DOMAIN}.po"
    mo_path = locale_dir / "LC_MESSAGES" / f"{DOMAIN}.mo"
    if not po_path.exists():
        return
    po = polib.pofile(str(po_path))
    po.save_as_mofile(str(mo_path))


def main() -> int:
    if not LOCALES_DIR.exists():
        return 0
    for loc in LOCALES_DIR.iterdir():
        compile_locale(loc)
    print("Compiled catalogs under", LOCALES_DIR)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


