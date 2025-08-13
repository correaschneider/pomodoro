from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto
from uuid import UUID


class SessionType(Enum):
    FOCUS = auto()
    BREAK = auto()


class TimerState(Enum):
    IDLE = auto()
    RUNNING_FOCUS = auto()
    RUNNING_BREAK = auto()
    PAUSED = auto()


@dataclass
class Session:
    id: UUID
    type: SessionType
    duration_s: int
    started_at: datetime | None
    ended_at: datetime | None
    state: TimerState


