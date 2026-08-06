from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

from domain.errors import (
    BlueprintNotFoundError,
    ComponentNotFoundError,
    DependencyCycleError,
    EngineNotFoundError,
)
from domain.manifest import (
    BlueprintManifest,
    ComponentManifest,
    load_blueprint_manifest,
    load_component_manifest,
)

BLUEPRINTS_DIRNAME = "blueprints"
COMPONENTS_DIRNAME = "components"


@dataclass(frozen=True)
class ResolvedBlueprint:
    name: str
    path: Path
    manifest: BlueprintManifest


@dataclass(frozen=True)
class ResolvedComponent:
    name: str
    path: Path
    manifest: ComponentManifest


def _list_catalog_entries(catalog_root: Path, subdir: str) -> list[str]:
    base = catalog_root / subdir
    if not base.is_dir():
        return []
    return sorted(p.name for p in base.iterdir() if p.is_dir())


class BlueprintResolver:
    def __init__(self, catalog_root: Path, known_engines: Iterable[str]):
        self._catalog_root = catalog_root
        self._known_engines = set(known_engines)

    def list_available(self) -> list[str]:
        return _list_catalog_entries(self._catalog_root, BLUEPRINTS_DIRNAME)

    def resolve(self, name: str) -> ResolvedBlueprint:
        blueprint_dir = self._catalog_root / BLUEPRINTS_DIRNAME / name
        if not blueprint_dir.is_dir():
            raise BlueprintNotFoundError(f"blueprint '{name}' não encontrado no catálogo")
        manifest = load_blueprint_manifest(blueprint_dir)
        if manifest.engine not in self._known_engines:
            raise EngineNotFoundError(
                f"engine '{manifest.engine}' declarada pelo blueprint '{name}' não está registrada"
            )
        return ResolvedBlueprint(name=name, path=blueprint_dir, manifest=manifest)


class ComponentResolver:
    def __init__(self, catalog_root: Path):
        self._catalog_root = catalog_root

    def list_available(self) -> list[str]:
        return _list_catalog_entries(self._catalog_root, COMPONENTS_DIRNAME)

    def _load(self, name: str, requested_by: str | None = None) -> ComponentManifest:
        component_dir = self._catalog_root / COMPONENTS_DIRNAME / name
        if not component_dir.is_dir():
            origin = f" (dependência de '{requested_by}')" if requested_by else ""
            raise ComponentNotFoundError(f"component '{name}' não encontrado no catálogo{origin}")
        return load_component_manifest(component_dir)

    def resolve(self, names: list[str]) -> list[ResolvedComponent]:
        manifests: dict[str, ComponentManifest] = {}

        def load_recursive(name: str, requested_by: str | None) -> None:
            if name in manifests:
                return
            manifest = self._load(name, requested_by)
            manifests[name] = manifest
            for dep in manifest.depends_on:
                load_recursive(dep, name)

        for name in names:
            load_recursive(name, None)

        ordered: list[str] = []
        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(name: str, path: list[str]) -> None:
            if name in visited:
                return
            if name in visiting:
                cycle = " -> ".join(path[path.index(name):] + [name])
                raise DependencyCycleError(f"ciclo de dependência detectado entre components: {cycle}")
            visiting.add(name)
            for dep in manifests[name].depends_on:
                visit(dep, path + [name])
            visiting.remove(name)
            visited.add(name)
            ordered.append(name)

        for name in manifests:
            visit(name, [])

        return [
            ResolvedComponent(
                name=name,
                path=self._catalog_root / COMPONENTS_DIRNAME / name,
                manifest=manifests[name],
            )
            for name in ordered
        ]
