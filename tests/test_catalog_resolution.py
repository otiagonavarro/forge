import pytest

from domain.catalog import BlueprintResolver, ComponentResolver
from domain.errors import (
    BlueprintNotFoundError,
    ComponentNotFoundError,
    DependencyCycleError,
    EngineNotFoundError,
)


def test_blueprint_resolve_not_found(catalog_root):
    resolver = BlueprintResolver(catalog_root, known_engines={"cookiecutter"})
    with pytest.raises(BlueprintNotFoundError):
        resolver.resolve("does-not-exist")


def test_blueprint_resolve_unknown_engine(catalog_root):
    resolver = BlueprintResolver(catalog_root, known_engines={"cookiecutter"})
    with pytest.raises(EngineNotFoundError):
        resolver.resolve("bad-engine-blueprint")


def test_blueprint_resolve_success(catalog_root):
    resolver = BlueprintResolver(catalog_root, known_engines={"cookiecutter"})
    resolved = resolver.resolve("sample-service")
    assert resolved.name == "sample-service"
    assert resolved.manifest.engine == "cookiecutter"


def test_blueprint_list_available(catalog_root):
    resolver = BlueprintResolver(catalog_root, known_engines={"cookiecutter"})
    assert "sample-service" in resolver.list_available()


def test_component_resolve_not_found(catalog_root):
    resolver = ComponentResolver(catalog_root)
    with pytest.raises(ComponentNotFoundError):
        resolver.resolve(["does-not-exist"])


def test_component_resolve_includes_transitive_dependency_ordered(catalog_root):
    resolver = ComponentResolver(catalog_root)
    resolved = resolver.resolve(["logging"])
    names = [component.name for component in resolved]
    assert names.index("secret-manager") < names.index("logging")


def test_component_resolve_cycle_detected(cycle_catalog_root):
    resolver = ComponentResolver(cycle_catalog_root)
    with pytest.raises(DependencyCycleError):
        resolver.resolve(["comp-a"])
