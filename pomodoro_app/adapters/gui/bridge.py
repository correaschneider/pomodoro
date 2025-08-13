from __future__ import annotations

from typing import Callable

from PySide6 import QtCore

from pomodoro_app.core.models import TimerState
from pomodoro_app.core.timer_service import TimerService
from pomodoro_app.infrastructure.logging import get_logger


logger = get_logger("pomodoro.adapters.gui.bridge")


class GuiBridge(QtCore.QObject):
    """Qt bridge object exposing signals for cross-thread updates.

    Signals are emitted via queued connections to ensure thread-safety when
    receiving callbacks from the domain thread.
    """

    tick = QtCore.Signal(int, int, object)  # elapsed, remaining, state (TimerState)
    state = QtCore.Signal(object)  # new state (TimerState)
    cycle_end = QtCore.Signal(object)  # finished Session

    def __init__(self) -> None:
        super().__init__()


def _queue_emit(signal: QtCore.SignalInstance, *args: object) -> None:
    """Emit a Qt signal from any thread using a queued connection."""
    # Using a lambda preserves args and ensures queued delivery to the GUI thread
    QtCore.QMetaObject.invokeMethod(
        signal,  # type: ignore[arg-type]
        "emit",
        QtCore.Qt.QueuedConnection,
        *[QtCore.QGenericArgument(type(arg).__name__, arg) for arg in args],
    )


def connect_service_to_bridge(service: TimerService, bridge: GuiBridge) -> Callable[[], None]:
    """Wire TimerService callbacks to Qt signals via queued emission.

    Returns an unsubscribe callable to detach all observers.
    """

    # Register callbacks on the service; capture minimal work in the callback
    def on_tick(elapsed: int, remaining: int, state: TimerState) -> None:
        try:
            bridge.tick.emit(elapsed, remaining, state)
        except RuntimeError:
            # If the bridge is deleted, guard against runtime errors from Qt
            logger.debug("tick emit skipped: bridge deleted")

    def on_state(state: TimerState) -> None:
        try:
            bridge.state.emit(state)
        except RuntimeError:
            logger.debug("state emit skipped: bridge deleted")

    def on_cycle_end(session: object) -> None:
        try:
            bridge.cycle_end.emit(session)
        except RuntimeError:
            logger.debug("cycle_end emit skipped: bridge deleted")

    unsub_tick = service.on_tick(on_tick)
    unsub_state = service.on_state(on_state)
    unsub_end = service.on_cycle_end(on_cycle_end)

    logger.info("GuiBridge connected to TimerService callbacks")

    def unsubscribe() -> None:
        unsub_tick()
        unsub_state()
        unsub_end()
        logger.info("GuiBridge disconnected from TimerService callbacks")

    return unsubscribe


__all__ = [
    "GuiBridge",
    "connect_service_to_bridge",
]


