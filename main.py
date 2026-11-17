"""Entry point. Jalankan: uv run python main.py"""
import os
import sys

# Mode --windowed (exe tanpa console) membuat stdout/stderr bernilai None.
if sys.stdout is None:
    sys.stdout = open(os.devnull, "w")
if sys.stderr is None:
    sys.stderr = open(os.devnull, "w")

from app.bootstrap import run  # noqa: E402

if __name__ == "__main__":
    run()
