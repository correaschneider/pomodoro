# PyInstaller spec for Pomodoro App
# Scope: Subtask 10.1 – Create PyInstaller spec (do not perform local build here)

import sys
from pathlib import Path

from PyInstaller.utils.hooks import (
    collect_submodules,
    collect_dynamic_libs,
)


# Project paths
project_root = Path.cwd().resolve()
entry_script = project_root / "pomodoro_app" / "__main__.py"

# Hidden imports: ensure PySide6 modules, pluggy, and packaging are discovered
hiddenimports = []
hiddenimports += [
    "PySide6.QtCore",
    "PySide6.QtGui",
    "PySide6.QtWidgets",
]
hiddenimports += collect_submodules("pluggy")
hiddenimports += collect_submodules("packaging")

# Datas: include compiled locale catalogs (.mo)
datas = []
locales_dir = project_root / "resources" / "locales"
if locales_dir.exists():
    for mo_file in locales_dir.rglob("*.mo"):
        # Place files under their relative directory within the bundle
        dest_dir = str(mo_file.parent.relative_to(project_root))
        datas.append((str(mo_file), dest_dir))

# Binaries: dynamic libraries for PySide6/Qt (platform plugins, etc.)
binaries = collect_dynamic_libs("PySide6")


a = Analysis(
    [str(entry_script)],
    pathex=[str(project_root)],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="pomodoro_app",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="pomodoro_app",
)
