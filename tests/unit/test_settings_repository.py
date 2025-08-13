from __future__ import annotations

from pomodoro_app.infrastructure.db.connection import connect
from pomodoro_app.infrastructure.db.schema import ensure_schema
from pomodoro_app.infrastructure.db.repositories import SettingsRepository


def test_set_and_get_json_values() -> None:
    conn = connect()
    ensure_schema(conn)
    repo = SettingsRepository(conn)

    repo.set("durations", {"focus": 1500, "break": 300})
    repo.set("language", "pt_BR")
    repo.set("overlay", True)

    assert repo.get("durations") == {"focus": 1500, "break": 300}
    assert repo.get("language") == "pt_BR"
    assert repo.get("overlay") is True
    assert repo.get("missing", default=42) == 42
