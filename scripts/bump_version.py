#!/usr/bin/env python
"""Naikkan versi aplikasi di app/meta.py + pyproject.toml, dan buat heading di CHANGELOG.md.

Pemakaian:
    uv run python scripts/bump_version.py patch      # 0.1.0 -> 0.1.1
    uv run python scripts/bump_version.py minor      # 0.1.0 -> 0.2.0
    uv run python scripts/bump_version.py major      # 0.1.0 -> 1.0.0
    uv run python scripts/bump_version.py 2.3.4      # versi eksplisit

Catatan perubahan ditulis dulu di bawah "## [Unreleased]" pada CHANGELOG.md;
skrip ini mengubahnya jadi rilis versi baru.
"""
import datetime
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
META = ROOT / "app" / "meta.py"
PYPROJECT = ROOT / "pyproject.toml"
CHANGELOG = ROOT / "CHANGELOG.md"

META_RE = re.compile(r'^(APP_VERSION\s*=\s*)"([^"]+)"', re.M)
PYPROJECT_RE = re.compile(r'^(version\s*=\s*)"[^"]+"', re.M)


def next_version(current: str, kind: str) -> str:
    if re.fullmatch(r"\d+\.\d+\.\d+", kind):
        return kind
    major, minor, patch = (int(x) for x in current.split("."))
    if kind == "major":
        return f"{major + 1}.0.0"
    if kind == "minor":
        return f"{major}.{minor + 1}.0"
    if kind == "patch":
        return f"{major}.{minor}.{patch + 1}"
    sys.exit("Argumen harus patch | minor | major | X.Y.Z")


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    meta = META.read_text(encoding="utf-8")
    m = META_RE.search(meta)
    if not m:
        sys.exit("APP_VERSION tidak ditemukan di app/meta.py")
    old = m.group(2)
    new = next_version(old, sys.argv[1])

    META.write_text(META_RE.sub(rf'\g<1>"{new}"', meta, count=1), encoding="utf-8")
    py = PYPROJECT.read_text(encoding="utf-8")
    PYPROJECT.write_text(PYPROJECT_RE.sub(rf'\g<1>"{new}"', py, count=1), encoding="utf-8")

    cl = CHANGELOG.read_text(encoding="utf-8")
    marker_re = re.compile(r"^## \[Unreleased\][ \t]*$", re.M)
    if marker_re.search(cl):
        today = datetime.date.today().isoformat()
        cl = marker_re.sub(lambda m: f"{m.group(0)}\n\n## [{new}] - {today}", cl, count=1)
        CHANGELOG.write_text(cl, encoding="utf-8")
    else:
        print("PERINGATAN: heading '## [Unreleased]' tidak ada di CHANGELOG.md")

    print(f"Versi: {old} -> {new}")


if __name__ == "__main__":
    main()
