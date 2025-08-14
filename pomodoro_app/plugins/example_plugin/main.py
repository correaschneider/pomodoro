from __future__ import annotations

from pomodoro_app.plugin_manager.spec import hookimpl
from pomodoro_app.infrastructure.logging import get_logger


logger = get_logger("plugin.example")


@hookimpl
def on_app_start(app_ctx: dict) -> None:
    logger.info("example plugin started with ctx: %s", sorted(app_ctx.keys()))


@hookimpl
def on_timer_tick(elapsed: int, remaining: int, state: object) -> None:
    # Keep very light to avoid overhead
    if remaining % 10 == 0:
        logger.debug("tick: remaining=%s", remaining)


@hookimpl
def on_cycle_end(session: object) -> None:
    logger.info("cycle finished: %s", getattr(session, "id", None))


