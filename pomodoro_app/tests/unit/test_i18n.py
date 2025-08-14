from __future__ import annotations

from pathlib import Path

from pomodoro_app.infrastructure.i18n import install, gettext_, ngettext_, on_locale_change


def test_install_and_gettext_fallback() -> None:
    tr = install(None)
    assert gettext_("Hello") == "Hello"


def test_pluralization_basic() -> None:
    install(None)
    assert ngettext_("item", "items", 1) == "item"
    assert ngettext_("item", "items", 2) == "items"


def test_on_locale_change_notifies_listeners(tmp_path: Path) -> None:
    events: list[str | None] = []
    unsub = on_locale_change(lambda lang: events.append(lang))
    try:
        install("pt_BR")
        install("en_US")
    finally:
        unsub()
    assert events[-2:] == ["pt_BR", "en_US"]


