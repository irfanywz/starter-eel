"""Menyalakan Eel: init folder web, pilih browser (Chrome -> Edge), tutup app saat window ditutup."""
import logging
import os
import sys

import eel

from app import paths
from app.core.logger import install_excepthook, setup_logging
from app.meta import APP_NAME

WINDOW_SIZE = (1100, 720)
BROWSER_MODES = ("chrome", "edge")  # urutan percobaan

log = logging.getLogger(__name__)


def _on_close(page, sockets) -> None:
    """Dipanggil Eel saat sebuah window ditutup. Keluar jika tidak ada window tersisa."""
    if sockets:
        return
    log.info("Window ditutup, aplikasi keluar.")
    logging.shutdown()
    os._exit(0)


def _fatal(message: str) -> None:
    log.critical(message)
    if sys.platform == "win32":
        import ctypes

        ctypes.windll.user32.MessageBoxW(0, message, APP_NAME, 0x10)
    else:
        print(message, file=sys.stderr)


def run() -> None:
    root_log = setup_logging()
    install_excepthook(root_log)
    log.info("Mulai (frozen=%s, base=%s)", paths.FROZEN, paths.BASE_DIR)

    import app.api  # noqa: F401  (registrasi @eel.expose, harus sebelum eel.start)

    eel.init(str(paths.WEB_DIR))

    # Profil browser terpisah di folder Data: tidak bercampur dengan Chrome/Edge harian user.
    args = [f"--user-data-dir={paths.BROWSER_PROFILE_DIR}"]

    last_error = None
    for mode in BROWSER_MODES:
        try:
            eel.start(
                "index.html",
                mode=mode,
                size=WINDOW_SIZE,
                port=0,  # port acak yang bebas
                cmdline_args=args,
                close_callback=_on_close,
            )
            return
        except EnvironmentError as e:
            last_error = e
            log.warning("Mode %s tidak tersedia: %s", mode, e)

    _fatal(f"Chrome atau Edge tidak ditemukan.\nInstal salah satunya lalu coba lagi.\n\n{last_error}")
