# ARCHITECTURE

Dokumen ini ditulis supaya manusia **dan agent AI** bisa paham project ini dengan cepat.
Baca bagian "Aturan emas" dulu.

## Ringkasan
Aplikasi desktop: **Python (Eel)** sebagai backend + **HTML/CSS/JS murni** (tanpa bundler, tanpa framework)
sebagai UI. Eel membuka window Chrome/Edge dalam mode `--app` dan menghubungkannya ke Python lewat WebSocket.
Dikemas jadi exe memakai **PyInstaller** (onedir). Python dikelola dengan **uv**.

## Aturan emas
1. Nama & versi hanya didefinisikan di `app/meta.py` (jangan hardcode di tempat lain).
2. Semua path lewat `app/paths.py`. Semua data pengguna disimpan di `<Slug>_Data/`.
3. Python ↔ JS hanya lewat fungsi `@api("nama_api")` (Python) dan `App.api.call("nama_api", ...)` (JS).
4. Setiap perubahan: catat di `CHANGELOG.md` dan naikkan versi (`scripts/bump_version.py`).
5. Dependency di `pyproject.toml` ditulis dengan batas versi (`>=`), jangan tanpa versi.
6. UI dibuat semudah mungkin: form seminimal mungkin, input sesedikit mungkin.

## Struktur folder
```
.
├── main.py                  Entry point (hanya memanggil app.bootstrap.run)
├── build.py                 Build exe + zip
├── pyproject.toml           Dependency (uv) + versi
├── app/
│   ├── meta.py              APP_NAME, APP_SLUG, APP_VERSION  (sumber tunggal)
│   ├── paths.py             Semua path (beda otomatis antara dev dan exe)
│   ├── bootstrap.py         eel.init + eel.start, pilih Chrome→Edge, keluar saat window ditutup
│   ├── api/
│   │   ├── __init__.py      Daftar import modul API (agar ter-register)
│   │   ├── registry.py      Dekorator @api + envelope {ok,data,error}
│   │   ├── system.py        app_info, app_open_data_dir
│   │   └── settings.py      settings_get_all, settings_set
│   └── core/
│       ├── logger.py        Logging ke file + excepthook global
│       └── settings_store.py  Setting JSON (key wajib terdaftar di DEFAULTS)
├── web/                     Frontend (dibundel apa adanya ke exe)
│   ├── index.html           Shell: sidebar + #content + urutan <script>
│   ├── css/                 base.css (variabel tema), components.css (layout & komponen)
│   ├── js/
│   │   ├── core/            app.js (namespace App), api.js, toast.js, router.js
│   │   ├── pages/           satu file per halaman: App.pages.<id>
│   │   └── main.js          Init: ambil info/setting, tema, buka halaman awal
│   └── img/icon.png
├── assets/icon.ico          Icon exe
└── scripts/
    ├── bump_version.py      Naikkan versi + heading CHANGELOG
    └── rename_app.py        Ganti nama aplikasi
```

## Alur runtime
1. `main.py` → `bootstrap.run()`: setup log, import `app.api` (registrasi `@eel.expose`), `eel.init(web/)`.
2. `eel.start("index.html", mode="chrome"→"edge", port=0, ...)` membuka window; port acak bebas.
3. Browser memuat `index.html` → `/eel.js` → `js/main.js`.
4. `main.js` memanggil `app_info` & `settings_get_all`, menerapkan tema, membuka halaman `home`.
5. Saat window terakhir ditutup, `_on_close` mematikan proses (`os._exit(0)`).

## Kontrak API
Setiap fungsi API Python dibungkus `@api("nama")` dan **selalu** membalas:
```
{"ok": true,  "data": <hasil>}
{"ok": false, "error": "pesan"}
```
`App.api.call()` membongkar envelope: mengembalikan `data`, atau menampilkan toast error lalu `throw`.
Penamaan API: `<modul>_<aksi>` snake_case (nama menjadi identifier JS `eel.<nama>`, jadi tidak boleh ada titik/strip).

## Data & path
| Mode | BASE_DIR | Data | Resource web |
|------|----------|------|--------------|
| Dev (`uv run`) | root project | `<root>/<Slug>_Data/` | `<root>/web/` |
| Exe | folder `.exe` | `<folder exe>/<Slug>_Data/` | `<Slug>_System/web/` |

Isi `<Slug>_Data/`: `settings.json`, `logs/app.log`, `browser/` (profil browser aplikasi).
Data baru → taruh di sini, buat path-nya di `paths.py`.

## Build & rilis
`uv run python build.py` menjalankan PyInstaller dengan `--contents-directory <Slug>_System`
(menggantikan `_internal`), `--windowed`, `--icon assets/icon.ico`, `web/` ditambahkan via `--add-data`,
`--collect-data eel` (untuk `eel.js`) dan `--hidden-import bottle_websocket`.
Lalu membuat `dist/<Slug>/<Slug>_Data/` dan zip `dist/"<APP_NAME> <versi>".zip`
dengan root folder `<APP_NAME>` tanpa versi.

## Cara menambah fitur
**API baru**
1. Buat/ubah `app/api/<modul>.py`, pakai `@api("modul_aksi")`.
2. Jika modul baru, tambahkan di import `app/api/__init__.py`.
3. Panggil dari JS: `await App.api.call("modul_aksi", arg1, ...)`.

**Halaman baru**
1. Buat `web/js/pages/<id>.js` berisi `App.pages.<id> = { title, mount(el) { ... } }`.
2. Tambahkan `<script>` di `web/index.html` (sebelum `main.js`) dan tombol `.nav-item[data-page="<id>"]` di sidebar.

**Setting baru**
Tambahkan key + nilai default di `DEFAULTS` pada `app/core/settings_store.py`
(key di luar DEFAULTS ditolak). Baca/tulis lewat `settings_get_all` / `settings_set`.

## Batasan & jebakan
- **Bukan ES module**: JS memakai `<script>` biasa + namespace `window.App`. Alasan: server Eel/bottle
  di Windows bisa mengirim `.js` dengan MIME salah sehingga `type="module"` gagal.
- **Tidak ada frameless / custom titlebar / tray**: window dikendalikan browser (Chrome/Edge `--app`).
  Butuh itu → pakai starter PySide6/Tkinter/Electron.
- `--windowed` membuat `sys.stdout/stderr` = `None`; `main.py` menggantinya ke devnull. Lihat log di file.
- Browser Chrome/Edge harus terpasang di komputer pengguna.
- Jangan memanggil `eel.*` langsung di halaman; selalu lewat `App.api.call`.
