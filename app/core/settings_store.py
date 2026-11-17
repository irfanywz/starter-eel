"""Penyimpanan setting sederhana (JSON) di Data/settings.json.

Setting baru WAJIB didaftarkan di DEFAULTS (sekaligus jadi nilai awal).
"""
import json
import logging
import os
import threading

from app import paths

log = logging.getLogger(__name__)

DEFAULTS: dict = {
    "theme": "dark",  # "dark" | "light"
}

_lock = threading.RLock()
_cache: dict | None = None


def _load() -> dict:
    global _cache
    if _cache is None:
        data: dict = {}
        try:
            data = json.loads(paths.SETTINGS_FILE.read_text(encoding="utf-8"))
        except FileNotFoundError:
            pass
        except (ValueError, OSError):
            log.exception("settings.json rusak, pakai default")
        _cache = {**DEFAULTS, **{k: v for k, v in data.items() if k in DEFAULTS}}
    return _cache


def _save(data: dict) -> None:
    paths.ensure_dirs()
    tmp = paths.SETTINGS_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, paths.SETTINGS_FILE)  # atomic


def get_all() -> dict:
    with _lock:
        return dict(_load())


def get(key: str, default=None):
    with _lock:
        return _load().get(key, default)


def set_value(key: str, value) -> None:
    with _lock:
        if key not in DEFAULTS:
            raise KeyError(f"Setting tidak dikenal: {key}")
        data = _load()
        data[key] = value
        _save(data)
