from actions.base import Action
from domain.context import GenerationContext
from domain.errors import ActionError


class CreateDirectory(Action):
    def execute(self, context: GenerationContext) -> None:
        destination = context.destination
        if destination.exists() and any(destination.iterdir()):
            raise ActionError("CreateDirectory", f"destino '{destination}' já existe e não está vazio")
        destination.mkdir(parents=True, exist_ok=True)
