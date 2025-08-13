from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from pomodoro_app.infrastructure.logging import get_logger


logger = get_logger("pomodoro.infrastructure.db")


@dataclass(frozen=True)
class StatsResult:
    total_focus_seconds: int
    total_break_seconds: int
    interruptions: int
    sessions_count: int


class StatsService:
    """Compute statistics from the `sessions` table.

    Definitions:
      - total_focus_seconds: sum of nominal durations for FOCUS sessions completed within
        the given period.
      - total_break_seconds: sum of nominal durations for BREAK sessions within period.
      - interruptions: count of sessions whose actual elapsed time is strictly less than
        the nominal `duration_s` (i.e., user stopped early).
      - sessions_count: number of sessions started within period.
    """

    def __init__(self, conn: sqlite3.Connection) -> None:
        self._conn = conn

    def compute(self, start: datetime | None = None, end: datetime | None = None) -> StatsResult:
        where, params = self._build_where_clause(start, end)

        # Sum durations by type
        sums_row = self._conn.execute(
            f"""
            SELECT
                COALESCE(SUM(CASE WHEN type='FOCUS' THEN duration_s ELSE 0 END), 0) as focus_sum,
                COALESCE(SUM(CASE WHEN type='BREAK' THEN duration_s ELSE 0 END), 0) as break_sum,
                COUNT(*) as sessions_count
            FROM sessions
            {where}
            """,
            params,
        ).fetchone()
        focus_sum = int(sums_row[0]) if sums_row else 0
        break_sum = int(sums_row[1]) if sums_row else 0
        sessions_count = int(sums_row[2]) if sums_row else 0

        # Interruptions: ended early vs declared duration
        # Use julianday diff to compute elapsed seconds approximately
        intr_clauses: list[str] = []
        intr_params: list[Any] = []
        if start is not None:
            intr_clauses.append("started_at >= ?")
            intr_params.append(start.isoformat())
        if end is not None:
            intr_clauses.append("started_at <= ?")
            intr_params.append(end.isoformat())
        intr_clauses.extend(
            [
                "started_at IS NOT NULL",
                "ended_at IS NOT NULL",
                "(CAST(duration_s AS INTEGER) > CAST(ROUND((julianday(ended_at) - julianday(started_at)) * 86400.0) AS INTEGER))",
            ]
        )
        intr_where = ("WHERE " + " AND ".join(intr_clauses)) if intr_clauses else ""
        intr_row = self._conn.execute(
            f"SELECT COUNT(*) FROM sessions {intr_where}", intr_params
        ).fetchone()
        interruptions = int(intr_row[0]) if intr_row else 0

        return StatsResult(
            total_focus_seconds=focus_sum,
            total_break_seconds=break_sum,
            interruptions=interruptions,
            sessions_count=sessions_count,
        )

    @staticmethod
    def _build_where_clause(start: datetime | None, end: datetime | None) -> tuple[str, list[Any]]:
        clauses: list[str] = []
        params: list[Any] = []
        if start is not None:
            clauses.append("started_at >= ?")
            params.append(start.isoformat())
        if end is not None:
            clauses.append("started_at <= ?")
            params.append(end.isoformat())
        where = ("WHERE " + " AND ".join(clauses)) if clauses else ""
        return where, params


__all__ = ["StatsService", "StatsResult"]


