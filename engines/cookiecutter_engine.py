from pathlib import Path
from typing import Any

from cookiecutter.main import cookiecutter

from engines.base import ScaffoldEngine


class CookiecutterEngine(ScaffoldEngine):
    def render(self, template_path: Path, destination: Path, context: dict[str, Any]) -> None:
        extra_context = {**context, "project_slug": destination.name}
        cookiecutter(
            template=str(template_path),
            output_dir=str(destination.parent),
            no_input=True,
            extra_context=extra_context,
            overwrite_if_exists=True,
        )
