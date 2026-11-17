#!/usr/bin/env python
"""Ganti nama aplikasi di semua tempat yang perlu (meta.py, pyproject.toml, <title> web).

Pemakaian:
    uv run python scripts/rename_app.py "Nama Aplikasi"

  APP_NAME = "Nama Aplikasi"   (tampilan; root folder di zip)
  APP_SLUG = "NamaAplikasi"    (NamaAplikasi.exe, NamaAplikasi_Data, NamaAplikasi_System)
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def sub_file(path: Path, pattern: str, repl: str) -> None:
    text = path.read_text(encoding="utf-8")
    new, n = re.subn(pattern, lambda _m: repl, text, count=1, flags=re.M)
    if n == 0:
        sys.exit(f"Pola tidak ditemukan di {path.name}: {pattern}")
    path.write_text(new, encoding="utf-8")


def main() -> None:
    if len(sys.argv) != 2 or not sys.argv[1].strip():
        sys.exit(__doc__)
    name = " ".join(sys.argv[1].split())
    slug = name.replace(" ", "")
    if not re.fullmatch(r"[A-Za-z0-9_]+", slug):
        sys.exit("Nama hanya boleh huruf, angka, underscore, dan spasi.")
    project = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")

    sub_file(ROOT / "app" / "meta.py", r'^APP_NAME\s*=\s*"[^"]*"', f'APP_NAME = "{name}"')
    sub_file(ROOT / "app" / "meta.py", r'^APP_SLUG\s*=\s*"[^"]*"', f'APP_SLUG = "{slug}"')
    sub_file(ROOT / "pyproject.toml", r'^name\s*=\s*"[^"]*"', f'name = "{project}"')
    sub_file(ROOT / "web" / "index.html", r"<title>.*?</title>", f"<title>{name}</title>")
    print(f"Nama: {name} | slug: {slug} | project: {project}")
    print("Jangan lupa catat di CHANGELOG.md dan jalankan bump_version.py.")


if __name__ == "__main__":
    main()
