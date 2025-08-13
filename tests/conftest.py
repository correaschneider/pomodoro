import os
import pytest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Iterator

from pomodoro_app.infrastructure.db.connection import connect
from pomodoro_app.infrastructure.db.schema import ensure_schema


@pytest.fixture(autouse=True, scope="session")
def _qt_offscreen_env() -> None:
    # Use offscreen platform for headless test environments
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    os.environ.setdefault("QT_LOGGING_RULES", "*.debug=false;qt.qpa.*=false")


@pytest.fixture()
def temp_conn() -> Iterator[object]:
    """Yield an isolated SQLite connection backed by a temporary file."""
    with TemporaryDirectory() as td:
        db_path = Path(td) / "test.sqlite3"
        conn = connect(db_path)
        ensure_schema(conn)
        try:
            yield conn
        finally:
            try:
                conn.close()
            except Exception:
                pass


