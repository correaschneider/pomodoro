from __future__ import annotations

import ast
import sys
from pathlib import Path
from typing import Iterable, Set

import polib


ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = ROOT / "pomodoro_app"
LOCALES_DIR = ROOT / "resources" / "locales"
POT_PATH = LOCALES_DIR / "pomodoro_app.pot"


def iter_python_files(base: Path) -> Iterable[Path]:
    for path in base.rglob("*.py"):
        yield path


class StringExtractor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.msgids: Set[str] = set()

    def visit_Call(self, node: ast.Call) -> None:  # noqa: N802
        func_name = self._get_func_name(node.func)
        if func_name in {"_", "gettext_"}:
            if node.args and isinstance(node.args[0], ast.Str):
                self.msgids.add(node.args[0].s)
        elif func_name == "pgettext_":
            if len(node.args) >= 2 and isinstance(node.args[1], ast.Str):
                self.msgids.add(node.args[1].s)
        self.generic_visit(node)

    @staticmethod
    def _get_func_name(node: ast.AST) -> str:
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            return node.attr
        return ""


def build_pot(msgids: Set[str]) -> polib.POFile:
    pot = polib.POFile()
    pot.metadata = {
        "Project-Id-Version": "pomodoro_app",
        "POT-Creation-Date": "",
        "PO-Revision-Date": "",
        "Language": "",
        "Content-Type": "text/plain; charset=UTF-8",
        "Content-Transfer-Encoding": "8bit",
    }
    for msgid in sorted(msgids):
        pot.append(polib.POEntry(msgid=msgid, msgstr=""))
    return pot


def merge_into_locale(locale_po: Path, pot: polib.POFile) -> None:
    if not locale_po.exists():
        locale_po.parent.mkdir(parents=True, exist_ok=True)
        po = polib.POFile()
        po.metadata = {
            "Project-Id-Version": "pomodoro_app",
            "Language": locale_po.parent.parent.name,
            "Content-Type": "text/plain; charset=UTF-8",
        }
    else:
        po = polib.pofile(str(locale_po))

    existing = {e.msgid for e in po}
    for entry in pot:
        if entry.msgid not in existing:
            po.append(polib.POEntry(msgid=entry.msgid, msgstr=""))
    po.save(str(locale_po))


def main() -> int:
    extractor = StringExtractor()
    for py in iter_python_files(SRC_DIR):
        try:
            tree = ast.parse(py.read_text(encoding="utf-8"))
            extractor.visit(tree)
        except Exception:
            # Skip files that fail to parse
            continue

    if not LOCALES_DIR.exists():
        LOCALES_DIR.mkdir(parents=True, exist_ok=True)
    pot = build_pot(extractor.msgids)
    pot.save(str(POT_PATH))

    # Merge into known locales if present
    for loc in LOCALES_DIR.iterdir():
        lc_messages = loc / "LC_MESSAGES" / "pomodoro_app.po"
        if lc_messages.parent.is_dir():
            merge_into_locale(lc_messages, pot)

    print(f"Extracted {len(extractor.msgids)} messages → {POT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


