# Starter (Eel Python)

Base utama untuk aplikasi GUI **Eel Python** (backend Python + UI HTML/JS di window Chrome/Edge mode app).
Semua aplikasi baru dimulai dari sini supaya struktur foldernya selalu sama.
Penjelasan detail untuk manusia/AI: lihat [ARCHITECTURE.md](ARCHITECTURE.md).

## Persyaratan
- [uv](https://docs.astral.sh/uv/)
- Google Chrome atau Microsoft Edge terpasang (Edge sudah bawaan Windows 10/11)

## Menjalankan
```bash
uv sync
uv run python main.py
```

## Membuat aplikasi baru dari starter
1. Salin folder starter ini, ganti nama foldernya.
2. `uv run python scripts/rename_app.py "Nama Aplikasi"`
3. Mulai kerjakan fitur di `app/api/` (Python) dan `web/js/pages/` (UI).

## Build jadi exe
```bash
uv run python build.py
```
Hasil di `dist/`:
```
Nama Aplikasi 0.1.0.zip         <- bundle rilis
NamaAplikasi/
├── NamaAplikasi.exe
├── NamaAplikasi_System/        <- isi PyInstaller (pengganti _internal)
└── NamaAplikasi_Data/          <- semua data tersimpan di sini
```
Di dalam zip, root foldernya `Nama Aplikasi/` (tanpa versi).

## Mengubah versi
Catat perubahan di `CHANGELOG.md` (bagian `[Unreleased]`), lalu:
```bash
uv run python scripts/bump_version.py patch   # atau minor / major / X.Y.Z
```

## Catatan
- Window memakai title bar bawaan browser (Eel tidak mendukung frameless/tray).
- Profil browser aplikasi terpisah, disimpan di `<Slug>_Data/browser/`.
- Log ada di `<Slug>_Data/logs/app.log`.
