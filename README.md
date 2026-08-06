<!-- markdownlint-disable -->
<div align="center">
  <img src="./assets/logo.svg" alt="forge" width="200" />
    <h1>forge</h1>

[![Python](https://img.shields.io/badge/python-%3E%3D3.11-3776AB?logo=python&logoColor=white)](pyproject.toml)
[![Click](https://img.shields.io/badge/CLI-Click-000000?logo=gnubash&logoColor=white)](pyproject.toml)
[![Cookiecutter](https://img.shields.io/badge/engine-Cookiecutter-D4AA00)](pyproject.toml)
[![pytest](https://img.shields.io/badge/tests-pytest-0A9EDC?logo=pytest&logoColor=white)](pyproject.toml)
[![ruff](https://img.shields.io/badge/lint-ruff-261230)](pyproject.toml)
[![PyPI](https://img.shields.io/badge/PyPI-not%20published-red?logo=pypi&logoColor=white)](#getting-started)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

**Plataforma de engenharia que padroniza a criação de projetos GCP** (Cloud Run, Cloud Function, Dataflow, Vertex AI Agent, etc.) **a partir de Blueprints e Components reutilizáveis**, orquestrados por Agents e executados por Actions.

**Repository:** [github.com/tiagornandrade/forge](https://github.com/tiagornandrade/forge)

**Not on PyPI.** Install from a local clone (see below).

---

## Features

- **`forge create`** — gera um projeto novo a partir de um Blueprint do catálogo, no modo interativo (prompts) ou não interativo (`--blueprint`/`--name`/`--components`).
- **Blueprints** — manifesto `blueprint.yaml` descrevendo nome, versão, `ScaffoldEngine` a usar e arquivos obrigatórios pós-geração.
- **Components** — manifesto `component.yaml` com dependências (`depends_on`), variáveis, arquivos e hooks (`after_install`); resolvidos e ordenados topologicamente, com detecção de ciclo.
- **Scaffold Engines** — abstração `ScaffoldEngine` + registry por nome; `CookiecutterEngine` é a implementação atual (Copier/Native ficam para roadmap futuro).
- **Pipeline de Actions** — `CreateDirectory → RenderBlueprint → InstallComponent → InitializeGit → ValidateProject`, cada uma com responsabilidade única e falha isolada (sem rollback automático — estado parcial é preservado para inspeção).
- **`BlueprintAgent`** — orquestra resolução de catálogo + execução do pipeline; não manipula arquivos diretamente.

Forge **não faz deploy**, não substitui Terraform/CI/CD nem frameworks internos — gera apenas a estrutura do projeto.

---

## Getting Started

### Clone + install (development)

```bash
git clone https://github.com/tiagornandrade/forge.git
cd forge
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

### Rodar o CLI

```bash
forge create
```

Modo interativo: escolhe Blueprint, Components (opcional) e nome do projeto no catálogo (`catalog/`).

Modo não interativo:

```bash
forge create --blueprint sample-service --name payments-api --components logging
```

O projeto é gerado em `./<name>`, relativo ao diretório atual.

---

## Verify

- Testes: **`pytest`** (fixtures isoladas em `tests/fixtures/`, nunca dependem de `catalog/` real).
- Lint: **`ruff check .`**
- CLI via `click.testing.CliRunner`:

```bash
pytest tests/test_cli.py -v
```

---

## Prerequisites

| Tool           | Required for               |
|----------------|-----------------------------|
| Python 3.11+   | Sempre                      |
| Git            | `InitializeGit` action e clone do repo |

---

## Architecture

Camadas do RFC, cada uma um pacote Python top-level (sem `src/` layout):

| Pacote | Responsabilidade |
|--------|-------------------|
| `domain/` | Manifestos (`blueprint.yaml`/`component.yaml`), `BlueprintResolver`/`ComponentResolver`, `GenerationContext`, erros de domínio |
| `actions/` | Contrato `Action.execute(context)` e Actions concretas (uma responsabilidade cada) |
| `engines/` | Abstração `ScaffoldEngine` + registry por nome; `CookiecutterEngine` é a implementação atual |
| `agents/` | `BlueprintAgent` orquestra resolução + pipeline de Actions; não manipula arquivos diretamente |
| `cli/` | Comando `forge create` (interativo e não interativo) |
| `catalog/` | Dados (Blueprints/Components reais), não código — vazio propositalmente; testes usam fixtures em `tests/fixtures/catalog/` |

---

## Catalog layout

```
catalog/
  blueprints/
    <nome>/
      blueprint.yaml       # name, version, engine, required_files
      <template files>
  components/
    <nome>/
      component.yaml       # name, version, dependencies, variables, files, hooks, depends_on
      <template files>
```

---

## CLI reference

| Command | Description |
|---------|-------------|
| `forge create` | Modo interativo — pergunta Blueprint, Components e nome |
| `forge create --blueprint <nome> --name <nome> [--components a,b]` | Modo não interativo |
| `forge --help` | Mostra uso |

---

## Configuration

Nenhum `.env`/segredo requerido no momento. Blueprints e Components reais entram via mudanças futuras (ver `openspec/`); `catalog/` fica vazio por design nesta fase.

---

## License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for details.
