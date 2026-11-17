"""Import semua modul API di sini supaya ter-register ke Eel sebelum eel.start().

Menambah API baru: buat app/api/<modul>.py lalu tambahkan import-nya di bawah.
"""
from app.api import settings, system  # noqa: F401
