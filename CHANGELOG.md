# Changelog

Format mengikuti [Keep a Changelog](https://keepachangelog.com/). Versi mengikuti SemVer.

**Aturan:** setiap perubahan dicatat di bawah `## [Unreleased]`, lalu jalankan
`uv run python scripts/bump_version.py patch|minor|major` — skrip itu menaikkan versi
(`app/meta.py` + `pyproject.toml`) dan mengubah catatan Unreleased menjadi rilis baru.

## [Unreleased]

## [0.1.0] - 2026-11-17
### Ditambahkan
- Starter Eel Python pertama: layout sidebar, halaman Beranda / Pengaturan / Tentang.
- Kontrak API seragam `{ok, data, error}` lewat dekorator `@api`.
- Penyimpanan setting JSON (`<Slug>_Data/settings.json`), tema gelap/terang, toast.
- Logging ke `<Slug>_Data/logs/app.log` dan penangkap error global.
- `build.py`: build PyInstaller (`<Slug>.exe` + `<Slug>_System/` + `<Slug>_Data/`) dan zip `"<Nama> <versi>.zip"`.
- Skrip `bump_version.py` dan `rename_app.py`.
- Icon aplikasi (`assets/icon.ico`, `web/img/icon.png`).
