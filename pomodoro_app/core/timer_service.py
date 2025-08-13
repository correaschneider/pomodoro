from __future__ import annotations

import logging
import threading
from typing import Callable, Literal

from .models import Session, SessionType, TimerState
from .ports import (
    CYCLE_END_CALLBACKS,
    STATE_CALLBACKS,
    TICK_CALLBACKS,
    CycleEndCallback,
    StateCallback,
    TickCallback,
)


class TimerService:
    """Skeleton for the TimerService; ticking loop is implemented in subtask 2.4."""

    def __init__(
        self,
        tick_interval: float = 1.0,
        clock: Callable[[], float] | None = None,
        logger: logging.Logger | None = None,
    ) -> None:
        if tick_interval <= 0:
            raise ValueError("tick_interval must be > 0")
        self._tick_interval: float = tick_interval
        self._clock: Callable[[], float] = clock or __import__("time").monotonic
        self._logger: logging.Logger = logger or logging.getLogger("pomodoro.core")

        self.state: TimerState = TimerState.IDLE
        self._remaining: float = 0.0
        self._current_session: Session | None = None

        self._lock = threading.RLock()
        self._thread: threading.Thread | None = None
        self._shutdown_event = threading.Event()

        # Local observer registry; service-level callbacks (separate from module-level)
        self._observers: dict[str, set[Callable[..., None]]] = {
            "tick": set(),
            "cycle_end": set(),
            "state": set(),
        }

    # Observer registration -----------------------------------------------------
    def on_tick(self, callback: TickCallback) -> Callable[[], None]:
        return self.on("tick", callback)

    def on_cycle_end(self, callback: CycleEndCallback) -> Callable[[], None]:
        return self.on("cycle_end", callback)

    def on_state(self, callback: StateCallback) -> Callable[[], None]:
        return self.on("state", callback)

    def on(self, event: Literal["tick", "cycle_end", "state"], callback: Callable[..., None]) -> Callable[[], None]:
        with self._lock:
            self._observers[event].add(callback)

        def _unsubscribe() -> None:
            with self._lock:
                self._observers[event].discard(callback)

        return _unsubscribe

    # API stubs (to be implemented in subsequent subtasks) ---------------------
    def start_focus(self, dur_s: int | None = None) -> None:
        raise NotImplementedError

    def start_break(self, dur_s: int | None = None) -> None:
        raise NotImplementedError

    def pause(self) -> None:
        raise NotImplementedError

    def resume(self) -> None:
        raise NotImplementedError

    def stop(self) -> None:
        raise NotImplementedError

    # Internal ticking loop (implemented for subtask 2.4) ---------------------
    def _spawn_thread(self) -> None:
        with self._lock:
            if self._thread and self._thread.is_alive():
                return
            self._shutdown_event.clear()
            self._thread = threading.Thread(target=self._run_loop, name="TimerServiceThread", daemon=True)
            self._thread.start()

    def _join_thread_if_running(self, timeout: float | None = None) -> None:
        with self._lock:
            thread = self._thread
        if thread and thread.is_alive():
            thread.join(timeout=timeout)

    def _elapsed(self, total_duration: float) -> float:
        return max(0.0, total_duration - self._remaining)

    def _run_loop(self) -> None:
        import time

        last = self._clock()
        while not self._shutdown_event.is_set():
            time.sleep(self._tick_interval)
            now = self._clock()

            with self._lock:
                # Only progress time while running; paused keeps last synced
                if self.state == TimerState.PAUSED:
                    last = now
                    continue

                if self.state not in (TimerState.RUNNING_FOCUS, TimerState.RUNNING_BREAK):
                    # Not actively running; end the loop gracefully
                    break

                delta = max(0.0, now - last)
                last = now
                self._remaining = max(0.0, self._remaining - delta)

                # Emission of events will be implemented in subtask 2.6
                # Example placeholder (intended): self._emit_tick()

                if self._remaining <= 0:
                    # Finishing the cycle logic is completed in later subtasks (2.5/2.6)
                    # For now, just transition to IDLE and break the loop
                    self.state = TimerState.IDLE
                    break


