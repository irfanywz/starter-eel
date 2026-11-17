"""Logging ke file (Data/logs/app.log) + penangkap error global."""
import logging
import sys
import threading
from logging.handlers import RotatingFileHandler

from app import paths
from app.meta import APP_SLUG


def setup_logging() -> logging.Logger:
    paths.ensure_dirs()
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    fh = RotatingFileHandler(paths.LOG_FILE, maxBytes=512 * 1024, backupCount=3, encoding="utf-8")
    fh.setFormatter(fmt)
    root.addHandler(fh)

    if not paths.FROZEN:  # saat dev, log juga tampil di terminal
        sh = logging.StreamHandler()
        sh.setFormatter(fmt)
        root.addHandler(sh)
    return logging.getLogger(APP_SLUG)


def install_excepthook(log: logging.Logger) -> None:
    def _hook(exc_type, exc, tb):
        log.critical("Uncaught exception", exc_info=(exc_type, exc, tb))

    def _thread_hook(args):
        log.critical("Uncaught thread exception",
                     exc_info=(args.exc_type, args.exc_value, args.exc_traceback))

    sys.excepthook = _hook
    threading.excepthook = _thread_hook
