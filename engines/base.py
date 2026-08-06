from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from domain.errors import EngineNotFoundError


class ScaffoldEngine(ABC):
    @abstractmethod
    def render(self, template_path: Path, destination: Path, context: dict[str, Any]) -> None:
        ...


_REGISTRY: dict[str, ScaffoldEngine] = {}


def register_engine(name: str, engine: ScaffoldEngine) -> None:
    _REGISTRY[name] = engine


def get_engine(name: str) -> ScaffoldEngine:
    try:
        return _REGISTRY[name]
    except KeyError:
        raise EngineNotFoundError(f"scaffold engine '{name}' não registrada") from None


def list_engines() -> list[str]:
    return sorted(_REGISTRY.keys())
