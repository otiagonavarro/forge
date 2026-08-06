from actions.base import Action
from domain.context import GenerationContext
from domain.errors import ActionError


class ValidateProject(Action):
    def execute(self, context: GenerationContext) -> None:
        missing: list[str] = []

        missing.extend(
            rel_file
            for rel_file in context.blueprint.manifest.required_files
            if not (context.destination / rel_file).exists()
        )
        for component in context.components:
            missing.extend(
                f"{component.name}:{rel_file}"
                for rel_file in component.manifest.files
                if not (context.destination / rel_file).exists()
            )
        if missing:
            raise ActionError(
                "ValidateProject", f"itens obrigatórios ausentes: {', '.join(missing)}"
            )
