import os
import pytest


@pytest.fixture(autouse=True, scope="session")
def _qt_offscreen_env() -> None:
    # Use offscreen platform for headless test environments
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    os.environ.setdefault("QT_LOGGING_RULES", "*.debug=false;qt.qpa.*=false")


