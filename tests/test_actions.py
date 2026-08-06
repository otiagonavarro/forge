import pytest

import engines  # noqa: F401  (bootstraps the scaffold engine registry)
from actions.create_directory import CreateDirectory
from actions.initialize_git import InitializeGit
from actions.install_component import InstallComponent
from actions.render_blueprint import RenderBlueprint
from actions.validate_project import ValidateProject
from domain.catalog import BlueprintResolver, ComponentResolver
from domain.context import GenerationContext
from domain.errors import ActionError
from engines.base import list_engines


def _make_context(catalog_root, tmp_path, blueprint_name="sample-service", component_names=None):
    blueprint_resolver = BlueprintResolver(catalog_root, known_engines=list_engines())
    component_resolver = ComponentResolver(catalog_root)
    blueprint = blueprint_resolver.resolve(blueprint_name)
    components = component_resolver.resolve(component_names or [])
    return GenerationContext(
        project_name=tmp_path.name,
        destination=tmp_path / "project",
        blueprint=blueprint,
        components=components,
    )


def test_create_directory_creates_empty_dir(catalog_root, tmp_path):
    context = _make_context(catalog_root, tmp_path)
    CreateDirectory().execute(context)
    assert context.destination.is_dir()


def test_create_directory_fails_if_not_empty(catalog_root, tmp_path):
    context = _make_context(catalog_root, tmp_path)
    context.destination.mkdir(parents=True)
    (context.destination / "existing.txt").write_text("x")

    with pytest.raises(ActionError):
        CreateDirectory().execute(context)


def test_render_blueprint_delegates_to_engine(catalog_root, tmp_path):
    context = _make_context(catalog_root, tmp_path)
    CreateDirectory().execute(context)
    RenderBlueprint().execute(context)

    assert (context.destination / "README.md").exists()


def test_install_component_copies_files_and_runs_hook(catalog_root, tmp_path):
    context = _make_context(catalog_root, tmp_path, component_names=["logging"])
    CreateDirectory().execute(context)

    InstallComponent().execute(context)

    assert (context.destination / "templates" / "secret_manager_client.py").exists()
    assert (context.destination / "templates" / "logging_client.py").exists()
    assert (context.destination / ".logging_hook_ran").exists()


def test_install_component_no_hook_declared(catalog_root, tmp_path):
    context = _make_context(catalog_root, tmp_path, component_names=["secret-manager"])
    CreateDirectory().execute(context)

    InstallComponent().execute(context)

    assert (context.destination / "templates" / "secret_manager_client.py").exists()


def test_initialize_git_creates_repo(catalog_root, tmp_path):
    context = _make_context(catalog_root, tmp_path)
    CreateDirectory().execute(context)

    InitializeGit().execute(context)

    assert (context.destination / ".git").is_dir()


def test_validate_project_fails_on_missing_required_file(catalog_root, tmp_path):
    context = _make_context(catalog_root, tmp_path)
    CreateDirectory().execute(context)

    with pytest.raises(ActionError):
        ValidateProject().execute(context)


def test_validate_project_passes_when_structure_complete(catalog_root, tmp_path):
    context = _make_context(catalog_root, tmp_path, component_names=["logging"])
    CreateDirectory().execute(context)
    RenderBlueprint().execute(context)
    InstallComponent().execute(context)

    ValidateProject().execute(context)
