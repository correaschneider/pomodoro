from __future__ import annotations

from typing import Any, Optional

import pluggy


PROJECT_NAME = "pomodoro_app"

hookspec = pluggy.HookspecMarker(PROJECT_NAME)
hookimpl = pluggy.HookimplMarker(PROJECT_NAME)


@hookspec
def on_app_start(app_ctx: dict[str, Any]) -> None:
    """Called once when the application starts.

    app_ctx exposes a restricted context (e.g., loggers, configuration). Plugins must not
    assume access to GUI or network unless explicitly allowed by permissions.
    """


@hookspec
def on_timer_tick(elapsed: int, remaining: int, state: object) -> None:
    """Called on each timer tick with elapsed/remaining seconds and current state."""


@hookspec
def on_cycle_end(session: object) -> None:
    """Called when a focus/break cycle ends with the finished session object."""


@hookspec
def provide_settings_ui(parent: object) -> Optional[object]:
    """Optionally return a QWidget-like settings panel for this plugin.

    Using a generic object type to avoid importing Qt at plugin discovery time.
    Implementations should return a QtWidgets.QWidget or None.
    """


__all__ = [
    "hookspec",
    "hookimpl",
    "on_app_start",
    "on_timer_tick",
    "on_cycle_end",
    "provide_settings_ui",
]


