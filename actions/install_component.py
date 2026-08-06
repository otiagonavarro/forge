import importlib.util
import shutil

from actions.base import Action
from domain.catalog import ResolvedComponent
from domain.context import GenerationContext
from domain.errors import ActionError


class InstallComponent(Action):
    def execute(self, context: GenerationContext) -> None:
        for component in context.components:
            self._install_one(component, context)

    def _install_one(self, component: ResolvedComponent, context: GenerationContext) -> None:
        try:
            for rel_file in component.manifest.files:
                src = component.path / rel_file
                dst = context.destination / rel_file
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)

            if hook_ref := component.manifest.hooks.get("after_install"):
                self._run_hook(hook_ref, component, context)
        except Exception as exc:
            raise ActionError(
                "InstallComponent", f"falha ao instalar component '{component.name}': {exc}"
            ) from exc

    def _run_hook(self, hook_ref: str, component: ResolvedComponent, context: GenerationContext) -> None:
        module_name, func_name = hook_ref.split(".", 1)
        module_path = component.path / f"{module_name}.py"
        spec = importlib.util.spec_from_file_location(f"{component.name}_{module_name}", module_path)
        if spec is None or spec.loader is None:
            raise ActionError("InstallComponent", f"hook module não encontrado: {module_path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        hook_func = getattr(module, func_name)
        hook_func(context)
