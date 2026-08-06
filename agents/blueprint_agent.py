from dataclasses import dataclass
from pathlib import Path
from typing import Any

from actions.create_directory import CreateDirectory
from actions.initialize_git import InitializeGit
from actions.install_component import InstallComponent
from actions.render_blueprint import RenderBlueprint
from actions.validate_project import ValidateProject
from domain.catalog import BlueprintResolver, ComponentResolver
from domain.context import GenerationContext


@dataclass(frozen=True)
class GenerationResult:
    success: bool
    destination: Path
    failed_action: str | None = None
    error: str | None = None


class BlueprintAgent:
    _PIPELINE = (
        CreateDirectory,
        RenderBlueprint,
        InstallComponent,
        InitializeGit,
        ValidateProject,
    )

    def __init__(self, blueprint_resolver: BlueprintResolver, component_resolver: ComponentResolver):
        self._blueprint_resolver = blueprint_resolver
        self._component_resolver = component_resolver

    def generate(
        self,
        blueprint_name: str,
        project_name: str,
        destination: Path,
        component_names: list[str] | None = None,
        variables: dict[str, Any] | None = None,
    ) -> GenerationResult:
        blueprint = self._blueprint_resolver.resolve(blueprint_name)
        components = self._component_resolver.resolve(list(component_names or []))

        context = GenerationContext(
            project_name=project_name,
            destination=destination,
            blueprint=blueprint,
            components=components,
            variables=variables or {},
        )

        for action_cls in self._PIPELINE:
            action = action_cls()
            try:
                action.execute(context)
            except Exception as exc:  # noqa: BLE001 - Action failures must not crash the pipeline
                return GenerationResult(
                    success=False,
                    destination=destination,
                    failed_action=action_cls.__name__,
                    error=str(exc),
                )

        return GenerationResult(success=True, destination=destination)
