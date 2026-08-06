import pytest

from domain.errors import ManifestNotFoundError
from domain.manifest import load_blueprint_manifest, load_component_manifest


def test_load_blueprint_manifest_valid(catalog_root):
    manifest = load_blueprint_manifest(catalog_root / "blueprints" / "sample-service")
    assert manifest.name == "sample-service"
    assert manifest.engine == "cookiecutter"
    assert manifest.required_files == ["README.md"]


def test_load_blueprint_manifest_missing_file(catalog_root):
    with pytest.raises(ManifestNotFoundError):
        load_blueprint_manifest(catalog_root / "blueprints" / "no-manifest-blueprint")


def test_load_component_manifest_valid(catalog_root):
    manifest = load_component_manifest(catalog_root / "components" / "logging")
    assert manifest.name == "logging"
    assert manifest.depends_on == ["secret-manager"]
    assert manifest.hooks == {"after_install": "hooks.after_install"}


def test_load_component_manifest_missing_file(catalog_root):
    with pytest.raises(ManifestNotFoundError):
        load_component_manifest(catalog_root / "components" / "does-not-exist")
