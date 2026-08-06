from engines.base import ScaffoldEngine, get_engine, list_engines, register_engine
from engines.cookiecutter_engine import CookiecutterEngine

register_engine("cookiecutter", CookiecutterEngine())

__all__ = [
    "CookiecutterEngine",
    "ScaffoldEngine",
    "get_engine",
    "list_engines",
    "register_engine",
]
