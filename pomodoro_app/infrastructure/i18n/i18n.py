from __future__ import annotations

import builtins
import gettext
from pathlib import Path
from typing import Optional, Callable

from pomodoro_app.infrastructure.logging import get_logger
from pomodoro_app.plugin_manager import get_plugin_domains


logger = get_logger("pomodoro.infrastructure.i18n")

# Project-wide gettext domain and locales directory
DOMAIN: str = "pomodoro_app"
LOCALES_DIR: Path = Path(__file__).resolve().parents[3] / "resources" / "locales"

# Keep a reference to the currently installed translation
_current_translation: gettext.NullTranslations = gettext.NullTranslations()
_current_language: Optional[str] = None
_listeners: set[Callable[[Optional[str]], None]] = set()


def load_locale(lang_code: Optional[str]) -> gettext.NullTranslations:
    """Load translation for the given language code with fallback.

    If lang_code is falsy, a NullTranslations is returned.
    """

    if not lang_code:
        return gettext.NullTranslations()
    try:
        translation = gettext.translation(DOMAIN, localedir=str(LOCALES_DIR), languages=[lang_code], fallback=True)
        # Merge plugin domains (if any) as nested translations under core
        for _name, locales_path in get_plugin_domains().items():
            try:
                plug_tr = gettext.translation(_name, localedir=str(locales_path), languages=[lang_code], fallback=True)
                translation.add_fallback(plug_tr)
            except Exception:
                # Ignore plugin errors but continue
                logger.debug("failed loading plugin domain: %s", _name)
        return translation
    except Exception:  # Defensive: never break startup due to i18n
        logger.exception("Failed to load translation for %s", lang_code)
        return gettext.NullTranslations()


def install(lang_code: Optional[str]) -> gettext.NullTranslations:
    """Install gettext functions for the given language at runtime.

    - Sets builtins._ to the selected translation's gettext
    - Exposes module-level helpers that use the active translation
    - Returns the installed translation object
    """

    global _current_translation
    translation = load_locale(lang_code)
    _current_translation = translation
    globals()["_current_language"] = lang_code

    try:
        builtins.__dict__["_"] = translation.gettext  # type: ignore[assignment]
    except Exception:
        logger.exception("Failed to install _ builtin for gettext")

    # Notify listeners of language change
    try:
        for cb in list(_listeners):
            try:
                cb(lang_code)
            except Exception:
                logger.exception("i18n listener failed")
    except Exception:
        logger.exception("failed notifying i18n listeners")

    return translation


def gettext_(message: str) -> str:
    """Translate a simple message using the active translation."""

    try:
        return _current_translation.gettext(message)
    except Exception:
        return message


def ngettext_(singular: str, plural: str, n: int) -> str:
    """Plural-aware translation using the active translation."""

    try:
        return _current_translation.ngettext(singular, plural, n)
    except Exception:
        return singular if n == 1 else plural


def pgettext_(context: str, message: str) -> str:
    """Contextual translation using the active translation (fallback safe)."""

    # GNUTranslations has pgettext since Python 3.8; provide a safe fallback
    tr = _current_translation
    pget = getattr(tr, "pgettext", None)
    if callable(pget):
        try:
            return pget(context, message)
        except Exception:
            pass
    # Fallback: concatenate context and message per gettext convention
    return gettext_(message)


def on_locale_change(callback: Callable[[Optional[str]], None]) -> Callable[[], None]:
    """Register a callback to be invoked when install() changes the locale.

    Returns an unsubscribe function.
    """

    _listeners.add(callback)

    def _unsubscribe() -> None:
        _listeners.discard(callback)

    return _unsubscribe


def current_language() -> Optional[str]:
    return _current_language


__all__ = [
    "DOMAIN",
    "LOCALES_DIR",
    "load_locale",
    "install",
    "gettext_",
    "ngettext_",
    "pgettext_",
    "on_locale_change",
    "current_language",
]
