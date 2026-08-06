# Project Context

## Purpose
Forge é uma plataforma de engenharia que padroniza a criação de projetos GCP (Cloud Run, Cloud Function, Dataflow, Vertex AI Agent, etc.) a partir de Blueprints e Components reutilizáveis, orquestrados por Agents e executados por Actions. Ver `.specflow/rfc-001-forge-plataforma-de-engenharia-para-geracao-projetos-gcp/spec.md` para a visão completa.

## Tech Stack
- Python >=3.11
- Cookiecutter (primeira Scaffold Engine; Copier/Native ficam para roadmap futuro)
- Click (CLI)
- PyYAML (manifestos de Blueprint/Component)
- pytest (testes), ruff (lint/format)

## Project Conventions

### Code Style
- ruff como linter/formatter (`pyproject.toml` define `line-length = 100`).
- Sem comentários explicando o óbvio; comentários só para decisões não óbvias.

### Architecture Patterns
Camadas do RFC, cada uma um pacote Python top-level (sem `src/` layout):
- `domain/`: manifestos (`blueprint.yaml`/`component.yaml`), `BlueprintResolver`/`ComponentResolver`, `GenerationContext`, erros de domínio.
- `actions/`: contrato `Action.execute(context)` e Actions concretas (uma responsabilidade cada).
- `engines/`: abstração `ScaffoldEngine` + registry por nome; `CookiecutterEngine` é a implementação atual.
- `agents/`: `BlueprintAgent` orquestra resolução + pipeline de Actions; não manipula arquivos diretamente.
- `cli/`: comando `forge create` (interativo e não interativo).
- `catalog/`: dados (Blueprints/Components reais), não código. Está vazio propositalmente até que blueprints/components entrem em mudanças futuras — testes usam fixtures em `tests/fixtures/catalog/`.

### Testing Strategy
- pytest com fixtures de catálogo isoladas em `tests/fixtures/` (nunca depender de conteúdo real em `catalog/`, que é vazio por design nesta fase).
- Testes de CLI via `click.testing.CliRunner` com `isolated_filesystem()`.

### Git Workflow
[Ainda não definido — usar convenção padrão do time até ser explicitado]

## Domain Context
Ver RFC-0001 para os 5 conceitos centrais: Blueprints, Components, Agents, Actions, Scaffold Engine. A mudança `add-forge-foundation` implementa apenas a camada Foundation (esqueleto arquitetural); Blueprints/Components reais e engines Copier/Native são roadmap futuro.

## Important Constraints
- Forge não faz deploy, não substitui Terraform/CI/CD nem frameworks internos — gera apenas a estrutura do projeto.
- `BlueprintAgent` não faz rollback automático em falha: estado parcial é preservado para inspeção.

## External Dependencies
- Biblioteca `cookiecutter` (renderização de templates).
