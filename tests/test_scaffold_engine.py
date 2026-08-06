import pytest

import engines  # noqa: F401  (bootstraps the scaffold engine registry)
from domain.errors import EngineNotFoundError
from engines.base import get_engine, list_engines
from engines.cookiecutter_engine import CookiecutterEngine


def test_cookiecutter_engine_registered():
    assert "cookiecutter" in list_engines()
    assert isinstance(get_engine("cookiecutter"), CookiecutterEngine)


def test_unregistered_engine_raises():
    with pytest.raises(EngineNotFoundError):
        get_engine("does-not-exist")


def test_cookiecutter_engine_render(catalog_root, tmp_path):
    engine = get_engine("cookiecutter")
    destination = tmp_path / "rendered-project"
    destination.mkdir()

    engine.render(
        template_path=catalog_root / "blueprints" / "sample-service",
        destination=destination,
        context={"description": "hello"},
    )

    readme = destination / "README.md"
    assert readme.exists()
    assert "rendered-project" in readme.read_text()
    assert "hello" in readme.read_text()
