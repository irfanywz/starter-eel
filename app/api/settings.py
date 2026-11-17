"""API setting."""
from app.api.registry import api
from app.core import settings_store


@api("settings_get_all")
def get_all() -> dict:
    return settings_store.get_all()


@api("settings_set")
def set_value(key: str, value) -> dict:
    settings_store.set_value(key, value)
    return settings_store.get_all()
