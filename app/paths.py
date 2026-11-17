"""Semua path aplikasi ada di sini. Modul lain WAJIB pakai ini, jangan hitung path sendiri.

Mode dev    : BASE_DIR = root project,            Data = <root>/<Slug>_Data
Mode frozen : BASE_DIR = folder tempat .exe,      Data = <folder exe>/<Slug>_Data
Resource read-only (web/) selalu dibaca dari RES_DIR.
"""
import sys
from pathlib import Path

from app.meta import APP_SLUG

FROZEN = bool(getattr(sys, "frozen", False))

if FROZEN:
    BASE_DIR = Path(sys.executable).resolve().parent
    RES_DIR = Path(getattr(sys, "_MEIPASS", BASE_DIR))  # = <Slug>_System/
else:
    BASE_DIR = Path(__file__).resolve().parent.parent
    RES_DIR = BASE_DIR

WEB_DIR = RES_DIR / "web"

DATA_DIR = BASE_DIR / f"{APP_SLUG}_Data"
LOG_DIR = DATA_DIR / "logs"
LOG_FILE = LOG_DIR / "app.log"
SETTINGS_FILE = DATA_DIR / "settings.json"
BROWSER_PROFILE_DIR = DATA_DIR / "browser"


def ensure_dirs() -> None:
    for d in (DATA_DIR, LOG_DIR):
        d.mkdir(parents=True, exist_ok=True)
