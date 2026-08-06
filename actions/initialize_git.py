import subprocess

from actions.base import Action
from domain.context import GenerationContext
from domain.errors import ActionError


class InitializeGit(Action):
    def execute(self, context: GenerationContext) -> None:
        try:
            subprocess.run(
                ["git", "init"],
                cwd=context.destination,
                check=True,
                capture_output=True,
            )
        except (subprocess.CalledProcessError, FileNotFoundError) as exc:
            raise ActionError("InitializeGit", f"falha ao inicializar repositório git: {exc}") from exc
