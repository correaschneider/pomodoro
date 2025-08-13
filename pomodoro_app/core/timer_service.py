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

    # API methods with state/reentrancy guards (subtask 2.5) -------------------
    def start_focus(self, dur_s: int | None = None) -> None:
        self._start(SessionType.FOCUS, dur_s)

    def start_break(self, dur_s: int | None = None) -> None:
        self._start(SessionType.BREAK, dur_s)

    def pause(self) -> None:
        with self._lock:
            if self.state not in (TimerState.RUNNING_FOCUS, TimerState.RUNNING_BREAK):
                raise RuntimeError("pause() only valid when timer is running")
            self.state = TimerState.PAUSED
            self._logger.info("Timer paused")
        self._emit("state", self.state)

    def resume(self) -> None:
        with self._lock:
            if self.state != TimerState.PAUSED:
                raise RuntimeError("resume() only valid when timer is paused")
            if not self._current_session:
                raise RuntimeError("no session to resume")
            self.state = (
                TimerState.RUNNING_FOCUS
                if self._current_session.type == SessionType.FOCUS
                else TimerState.RUNNING_BREAK
            )
            self._logger.info("Timer resumed")
        self._emit("state", self.state)

    def stop(self) -> None:
        from datetime import datetime

        # Signal loop to shutdown promptly
        self._shutdown_event.set()
        with self._lock:
            if self._current_session and self._current_session.ended_at is None:
                self._current_session.ended_at = datetime.now()
            self.state = TimerState.IDLE
            self._remaining = 0.0
            self._logger.info("Timer stopped")
        # Join thread outside of lock to avoid deadlocks
        self._join_thread_if_running(timeout=2.0)
        with self._lock:
            # Clear thread reference for idempotency and to allow restarts
            if self._thread and not self._thread.is_alive():
                self._thread = None
        self._emit("state", self.state)

    # Internal helpers ---------------------------------------------------------
    def _start(self, session_type: SessionType, dur_s: int | None) -> None:
        from datetime import datetime
        from uuid import uuid4

        DEFAULT_FOCUS_SECONDS = 25 * 60
        DEFAULT_BREAK_SECONDS = 5 * 60

        with self._lock:
            if self.state in (
                TimerState.RUNNING_FOCUS,
                TimerState.RUNNING_BREAK,
                TimerState.PAUSED,
            ):
                raise RuntimeError("timer already running or paused")

            duration = (
                (dur_s if dur_s is not None else DEFAULT_FOCUS_SECONDS)
                if session_type == SessionType.FOCUS
                else (dur_s if dur_s is not None else DEFAULT_BREAK_SECONDS)
            )
            if duration <= 0:
                raise ValueError("duration must be positive")

            self._current_session = Session(
                id=uuid4(),
                type=session_type,
                duration_s=int(duration),
                started_at=datetime.now(),
                ended_at=None,
                state=TimerState.IDLE,  # will be updated below
            )

            self._remaining = float(duration)
            self.state = (
                TimerState.RUNNING_FOCUS
                if session_type == SessionType.FOCUS
                else TimerState.RUNNING_BREAK
            )
            self._current_session.state = self.state
            self._logger.info(
                "Timer started: %s for %ss", session_type.name.lower(), int(duration)
            )

            # prepare and start loop
            self._shutdown_event.clear()
            self._spawn_thread()
        # Emit state change outside of lock
        self._emit("state", self.state)

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

    @property
    def is_running(self) -> bool:
        with self._lock:
            return self.state in (TimerState.RUNNING_FOCUS, TimerState.RUNNING_BREAK)

    @property
    def is_paused(self) -> bool:
        with self._lock:
            return self.state == TimerState.PAUSED

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

                # Prepare tick payload while holding the lock
                if self._current_session is not None:
                    elapsed_i = int(self._current_session.duration_s - self._remaining)
                    remaining_i = int(self._remaining)
                else:
                    elapsed_i = 0
                    remaining_i = int(self._remaining)
                state_now = self.state

                # Has the session finished?
                if self._remaining <= 0:
                    from datetime import datetime

                    finished_session = self._current_session
                    if finished_session is not None and finished_session.ended_at is None:
                        finished_session.ended_at = datetime.now()
                    # Transition to IDLE; emit outside the lock
                    self.state = TimerState.IDLE
                    state_after = self.state
                else:
                    finished_session = None
                    state_after = None

            # Outside lock: emit tick or cycle_end/state
            if finished_session is not None:
                self._emit("cycle_end", finished_session)
                self._emit("state", state_after or TimerState.IDLE)
                break
            else:
                self._emit("tick", elapsed_i, remaining_i, state_now)

    # Event emission helpers ---------------------------------------------------
    def _emit(self, event: Literal["tick", "cycle_end", "state"], *args: object) -> None:
        # Collect callbacks from service-local observers and module-level registries
        with self._lock:
            local_callbacks = list(self._observers[event])
        if event == "tick":
            module_callbacks = list(TICK_CALLBACKS)
        elif event == "cycle_end":
            module_callbacks = list(CYCLE_END_CALLBACKS)
        else:
            module_callbacks = list(STATE_CALLBACKS)

        callbacks: list[Callable[..., None]] = local_callbacks + module_callbacks
        for cb in callbacks:
            try:
                cb(*args)
            except Exception:
                # Never let a callback exception crash the service loop
                self._logger.exception("callback error in %s", event)


