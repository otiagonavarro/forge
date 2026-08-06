import shutil
from pathlib import Path

from click.testing import CliRunner

from cli.main import cli


def _prepare_isolated_catalog(catalog_root: Path, cwd: Path) -> None:
    shutil.copytree(catalog_root, cwd / "catalog")


def test_create_non_interactive_with_components(catalog_root):
    runner = CliRunner()
    with runner.isolated_filesystem() as cwd:
        _prepare_isolated_catalog(catalog_root, Path(cwd))

        result = runner.invoke(
            cli,
            [
                "create",
                "--blueprint",
                "sample-service",
                "--name",
                "payments-api",
                "--components",
                "logging",
            ],
        )

        assert result.exit_code == 0, result.output
        assert (Path(cwd) / "payments-api" / "README.md").exists()
        assert (Path(cwd) / "payments-api" / "templates" / "secret_manager_client.py").exists()


def test_create_non_interactive_without_components(catalog_root):
    runner = CliRunner()
    with runner.isolated_filesystem() as cwd:
        _prepare_isolated_catalog(catalog_root, Path(cwd))

        result = runner.invoke(
            cli,
            ["create", "--blueprint", "sample-service", "--name", "solo-lib"],
        )

        assert result.exit_code == 0, result.output
        assert (Path(cwd) / "solo-lib" / "README.md").exists()


def test_create_unknown_blueprint_fails_before_generation(catalog_root):
    runner = CliRunner()
    with runner.isolated_filesystem() as cwd:
        _prepare_isolated_catalog(catalog_root, Path(cwd))

        result = runner.invoke(
            cli,
            ["create", "--blueprint", "does-not-exist", "--name", "x"],
        )

        assert result.exit_code != 0
        assert not (Path(cwd) / "x").exists()


def test_create_interactive_flow(catalog_root):
    runner = CliRunner()
    with runner.isolated_filesystem() as cwd:
        _prepare_isolated_catalog(catalog_root, Path(cwd))

        result = runner.invoke(
            cli,
            ["create"],
            input="sample-service\nlogging\ninteractive-project\n",
        )

        assert result.exit_code == 0, result.output
        assert (Path(cwd) / "interactive-project" / "README.md").exists()
