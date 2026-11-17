"""API info aplikasi & aksi sistem."""
import os
import subprocess
import sys

from app import paths
from app.api.registry import api
from app.meta import APP_NAME, APP_SLUG, APP_VERSION


@api("app_info")
def app_info() -> dict:
    return {
        "name": APP_NAME,
        "slug": APP_SLUG,
        "version": APP_VERSION,
        "frozen": paths.FROZEN,
        "data_dir": str(paths.DATA_DIR),
    }


@api("app_open_data_dir")
def open_data_dir() -> None:
    paths.ensure_dirs()
    target = str(paths.DATA_DIR)
    if sys.platform == "win32":
        os.startfile(target)  # type: ignore[attr-defined]
    elif sys.platform == "darwin":
        subprocess.Popen(["open", target])
    else:
        subprocess.Popen(["xdg-open", target])
