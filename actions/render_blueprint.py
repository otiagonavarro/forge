from actions.base import Action
from domain.context import GenerationContext
from domain.errors import ActionError
from engines.base import get_engine


class RenderBlueprint(Action):
    def execute(self, context: GenerationContext) -> None:
        engine = get_engine(context.blueprint.manifest.engine)
        try:
            engine.render(
                template_path=context.blueprint.path,
                destination=context.destination,
                context=dict(context.variables),
            )
        except Exception as exc:
            raise ActionError("RenderBlueprint", f"falha ao renderizar blueprint '{context.blueprint.name}': {exc}") from exc
