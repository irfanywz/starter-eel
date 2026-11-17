"""Dekorator @api: cara TUNGGAL mengekspos fungsi Python ke JavaScript.

Semua fungsi API mengembalikan envelope seragam:
    {"ok": True,  "data": <hasil>}
    {"ok": False, "error": "<pesan>"}
Exception otomatis di-log dan dibungkus jadi envelope error.
"""
import functools
import logging

import eel

log = logging.getLogger("api")


def api(name: str):
    """Ekspos fungsi sebagai eel.<name>(...) di JS. Nama = <modul>_<aksi>, snake_case."""

    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                return {"ok": True, "data": fn(*args, **kwargs)}
            except Exception as e:  # noqa: BLE001
                log.exception("API %s gagal", name)
                return {"ok": False, "error": str(e) or e.__class__.__name__}

        eel.expose(name)(wrapper)
        return fn

    return decorator
