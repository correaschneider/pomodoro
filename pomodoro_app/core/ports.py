from __future__ import annotations

from typing import Callable, Protocol

from .models import Session, TimerState

# Typed callback aliases
TickCallback = Callable[[int, int, TimerState], None]
CycleEndCallback = Callable[[Session], None]
StateCallback = Callable[[TimerState], None]

# Minimal module-level registries for callbacks
TICK_CALLBACKS: set[TickCallback] = set()
CYCLE_END_CALLBACKS: set[CycleEndCallback] = set()
STATE_CALLBACKS: set[StateCallback] = set()


class TimerPort(Protocol):
    def start_focus(self, dur_s: int) -> None:
        ...

    def start_break(self, dur_s: int) -> None:
        ...

    def pause(self) -> None:
        ...

    def resume(self) -> None:
        ...

    def stop(self) -> None:
        ...

    # Registration methods for observers
    def on_tick(self, callback: TickCallback) -> None:
        ...

    def on_cycle_end(self, callback: CycleEndCallback) -> None:
        ...

    def on_state(self, callback: StateCallback) -> None:
        ...


