from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from domain.catalog import ResolvedBlueprint, ResolvedComponent


@dataclass
class GenerationContext:
    project_name: str
    destination: Path
    blueprint: ResolvedBlueprint
    components: list[ResolvedComponent]
    variables: dict[str, Any] = field(default_factory=dict)
