#!/usr/bin/env python
"""Build exe + bundle zip.

    uv run python build.py            # build + zip
    uv run python build.py --no-zip   # build saja

Hasil (folder dist/):
    <Slug>/                      <- folder hasil PyInstaller
        <Slug>.exe
        <Slug>_System/           <- isi PyInstaller (_internal yang di-rename)
        <Slug>_Data/             <- data aplikasi (dibuat kosong)
    <APP_NAME> <versi>.zip       <- root folder di dalam zip = "<APP_NAME>" (tanpa versi)
"""
import argparse
import os
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from app.meta import APP_NAME, APP_SLUG, APP_VERSION  # noqa: E402

DIST = ROOT / "dist"
BUILD = ROOT / "build"
ICON = ROOT / "assets" / "icon.ico"


def run_pyinstaller() -> Path:
    sep = ";" if os.name == "nt" else ":"
    cmd = [
        sys.executable, "-m", "PyInstaller", str(ROOT / "main.py"),
        "--noconfirm", "--clean", "--onedir", "--windowed",
        "--name", APP_SLUG,
        "--contents-directory", f"{APP_SLUG}_System",
        "--distpath", str(DIST),
        "--workpath", str(BUILD),
        "--specpath", str(BUILD),
        "--add-data", f"{ROOT / 'web'}{sep}web",
        "--collect-data", "eel",              # eel.js
        "--hidden-import", "bottle_websocket",
    ]
    if ICON.exists():
        cmd += ["--icon", str(ICON)]
    print(">>", " ".join(cmd))
    subprocess.run(cmd, check=True, cwd=ROOT)
    return DIST / APP_SLUG


def make_zip(src: Path) -> Path:
    """Zip isi `src` dengan root folder APP_NAME (tanpa versi)."""
    zip_path = DIST / f"{APP_NAME} {APP_VERSION}.zip"
    zip_path.unlink(missing_ok=True)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for p in sorted(src.rglob("*")):
            z.write(p, Path(APP_NAME) / p.relative_to(src))
    return zip_path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-zip", action="store_true", help="lewati pembuatan zip")
    args = ap.parse_args()

    shutil.rmtree(BUILD, ignore_errors=True)
    shutil.rmtree(DIST / APP_SLUG, ignore_errors=True)
    DIST.mkdir(exist_ok=True)

    out = run_pyinstaller()
    (out / f"{APP_SLUG}_Data").mkdir(exist_ok=True)
    print(f"\nBuild selesai: {out}")

    if not args.no_zip:
        print(f"Zip          : {make_zip(out)}")


if __name__ == "__main__":
    main()
