from pathlib import Path

import click

import engines  # noqa: F401  (bootstraps the scaffold engine registry)
from agents.blueprint_agent import BlueprintAgent
from domain.catalog import BlueprintResolver, ComponentResolver
from domain.errors import (
    BlueprintNotFoundError,
    ComponentNotFoundError,
    DependencyCycleError,
    EngineNotFoundError,
)
from engines.base import list_engines

CATALOG_ROOT = Path("catalog")


@click.group()
def cli() -> None:
    pass


@cli.command("create")
@click.option("--blueprint", default=None, help="Nome do Blueprint a utilizar")
@click.option("--name", default=None, help="Nome do projeto a ser gerado")
@click.option("--components", default=None, help="Lista de Components separada por vírgula")
def create(blueprint: str | None, name: str | None, components: str | None) -> None:
    blueprint_resolver = BlueprintResolver(CATALOG_ROOT, known_engines=list_engines())
    component_resolver = ComponentResolver(CATALOG_ROOT)
    agent = BlueprintAgent(blueprint_resolver, component_resolver)

    if blueprint is None:
        available_blueprints = blueprint_resolver.list_available()
        if not available_blueprints:
            click.echo("Nenhum Blueprint disponível no catálogo.")
            raise SystemExit(1)
        blueprint = click.prompt("Qual Blueprint deseja utilizar?", type=click.Choice(available_blueprints))

        available_components = component_resolver.list_available()
        component_list: list[str] = []
        if available_components:
            raw = click.prompt(
                f"Quais Components deseja instalar? ({', '.join(available_components)})"
                " [separados por vírgula, ou vazio]",
                default="",
                show_default=False,
            )
            component_list = [item.strip() for item in raw.split(",") if item.strip()]

        if name is None:
            name = click.prompt("Nome do projeto")
    else:
        component_list = [item.strip() for item in components.split(",") if item.strip()] if components else []
        if name is None:
            raise click.UsageError("--name é obrigatório em modo não interativo")

    try:
        blueprint_resolver.resolve(blueprint)
    except (BlueprintNotFoundError, EngineNotFoundError) as exc:
        click.echo(f"Erro: {exc}", err=True)
        raise SystemExit(1) from exc

    destination = Path.cwd() / name

    try:
        result = agent.generate(
            blueprint_name=blueprint,
            project_name=name,
            destination=destination,
            component_names=component_list,
        )
    except (BlueprintNotFoundError, ComponentNotFoundError, DependencyCycleError, EngineNotFoundError) as exc:
        click.echo(f"Erro: {exc}", err=True)
        raise SystemExit(1) from exc

    if not result.success:
        click.echo(f"Falha na etapa {result.failed_action}: {result.error}", err=True)
        raise SystemExit(1)

    click.echo(f"Projeto gerado em {result.destination}")


if __name__ == "__main__":
    cli()
