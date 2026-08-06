from dataclasses import dataclass, field
from pathlib import Path

import yaml

from domain.errors import ManifestInvalidError, ManifestNotFoundError

BLUEPRINT_MANIFEST_FILENAME = "blueprint.yaml"
COMPONENT_MANIFEST_FILENAME = "component.yaml"


@dataclass(frozen=True)
class BlueprintManifest:
    name: str
    version: str
    engine: str
    required_files: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ComponentManifest:
    name: str
    version: str
    dependencies: list[str] = field(default_factory=list)
    variables: list[str] = field(default_factory=list)
    files: list[str] = field(default_factory=list)
    hooks: dict[str, str] = field(default_factory=dict)
    depends_on: list[str] = field(default_factory=list)


def _load_yaml(manifest_path: Path) -> dict:
    if not manifest_path.exists():
        raise ManifestNotFoundError(f"manifesto não encontrado: {manifest_path}")
    with manifest_path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def load_blueprint_manifest(blueprint_dir: Path) -> BlueprintManifest:
    data = _load_yaml(blueprint_dir / BLUEPRINT_MANIFEST_FILENAME)
    try:
        return BlueprintManifest(
            name=data["name"],
            version=str(data["version"]),
            engine=data["engine"],
            required_files=list(data.get("required_files", [])),
        )
    except KeyError as exc:
        raise ManifestInvalidError(
            f"campo obrigatório ausente em {blueprint_dir / BLUEPRINT_MANIFEST_FILENAME}: {exc}"
        ) from exc


def load_component_manifest(component_dir: Path) -> ComponentManifest:
    data = _load_yaml(component_dir / COMPONENT_MANIFEST_FILENAME)
    try:
        return ComponentManifest(
            name=data["name"],
            version=str(data["version"]),
            dependencies=list(data.get("dependencies", [])),
            variables=list(data.get("variables", [])),
            files=list(data.get("files", [])),
            hooks=dict(data.get("hooks", {})),
            depends_on=list(data.get("depends_on", [])),
        )
    except KeyError as exc:
        raise ManifestInvalidError(
            f"campo obrigatório ausente em {component_dir / COMPONENT_MANIFEST_FILENAME}: {exc}"
        ) from exc
