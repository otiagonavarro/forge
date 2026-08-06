import contextlib

import engines  # noqa: F401  (bootstraps the scaffold engine registry)
from agents.blueprint_agent import BlueprintAgent
from domain.catalog import BlueprintResolver, ComponentResolver
from domain.errors import BlueprintNotFoundError, ComponentNotFoundError
from engines.base import list_engines


def _make_agent(catalog_root):
    blueprint_resolver = BlueprintResolver(catalog_root, known_engines=list_engines())
    component_resolver = ComponentResolver(catalog_root)
    return BlueprintAgent(blueprint_resolver, component_resolver)


def test_full_pipeline_success(catalog_root, tmp_path):
    agent = _make_agent(catalog_root)
    destination = tmp_path / "my-project"

    result = agent.generate(
        blueprint_name="sample-service",
        project_name="my-project",
        destination=destination,
        component_names=["logging"],
    )

    assert result.success
    assert (destination / "README.md").exists()
    assert (destination / "templates" / "secret_manager_client.py").exists()
    assert (destination / ".git").is_dir()


def test_blueprint_resolution_failure_creates_no_files(catalog_root, tmp_path):
    agent = _make_agent(catalog_root)
    destination = tmp_path / "my-project"

    with contextlib.suppress(BlueprintNotFoundError):
        agent.generate(blueprint_name="does-not-exist", project_name="my-project", destination=destination)
        assert False, "expected BlueprintNotFoundError"
    assert not destination.exists()


def test_component_resolution_failure_creates_no_files(catalog_root, tmp_path):
    agent = _make_agent(catalog_root)
    destination = tmp_path / "my-project"

    with contextlib.suppress(ComponentNotFoundError):
        agent.generate(
            blueprint_name="sample-service",
            project_name="my-project",
            destination=destination,
            component_names=["does-not-exist"],
        )
        assert False, "expected ComponentNotFoundError"
    assert not destination.exists()


def test_pipeline_stops_at_failing_action_and_preserves_partial_state(catalog_root, tmp_path):
    agent = _make_agent(catalog_root)
    destination = tmp_path / "my-project"

    result = agent.generate(
        blueprint_name="sample-service",
        project_name="my-project",
        destination=destination,
        component_names=["broken-hook"],
    )

    assert not result.success
    assert result.failed_action == "InstallComponent"
    # RenderBlueprint (etapa anterior) já rodou e deixou estado parcial
    assert (destination / "README.md").exists()
    # InitializeGit e ValidateProject (etapas seguintes) não rodaram
    assert not (destination / ".git").exists()
