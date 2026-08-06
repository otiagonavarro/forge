# Change: Fundação da Plataforma Forge (Foundation)

## Why

Hoje projetos GCP (Cloud Run, Cloud Function, Dataflow, Vertex AI Agent, etc.) são criados copiando configuração manualmente entre repositórios (Docker, logging, IAM, Terraform, Cloud Build, GitHub Actions, testes). Isso gera duplicação, inconsistência arquitetural e alto custo de manutenção quando um padrão precisa evoluir (ver RFC-0001).

Esta mudança implementa a camada **Foundation** do Forge descrita no RFC: o esqueleto arquitetural (CLI, Domain, Agents, Actions, Scaffold Engine) capaz de orquestrar a geração de projetos a partir de Blueprints e Components, sem ainda incluir conteúdo real de blueprints/components — esses entram em mudanças subsequentes (roadmap "Blueprints", "Components" do RFC).

## What Changes

- **ADDED** `catalog-resolution`: estrutura de catálogo (`catalog/blueprints/`, `catalog/components/`), schema de manifesto (`blueprint.yaml`, `component.yaml`) e resolução de Blueprint/Components (incluindo `depends_on` com ordenação topológica e detecção de ciclo).
- **ADDED** `action-framework`: contrato `Action.execute(context)` e as Actions de fundação: `CreateDirectory`, `RenderBlueprint`, `InstallComponent`, `InitializeGit`, `ValidateProject`.
- **ADDED** `scaffold-engine`: abstração `ScaffoldEngine.render(...)` desacoplada de ferramenta, com primeira implementação `CookiecutterEngine`. `Copier`/`Native Engine` ficam fora de escopo (roadmap futuro).
- **ADDED** `generation-agent`: `BlueprintAgent`, orquestrador que interpreta a entrada, resolve Blueprint/Components e executa as Actions em sequência, sem manipular arquivos diretamente.
- **ADDED** `forge-cli`: comando `forge create` em modo interativo e não interativo (`--blueprint`, `--name`, `--components`).

Fora de escopo desta mudança (roadmap futuro do RFC):

- Blueprints reais (Cloud Run, Cloud Function, Dataflow, etc.) — cadastrados apenas como fixtures de teste nesta mudança.
- Components reais (BigQuery, Pub/Sub, Secret Manager, etc.) e Actions específicas de merge (`UpdatePyProject`, `UpdateDockerfile`, `UpdateTerraform`).
- Engines Copier e Native.
- Marketplace (`forge search/install/update`).

## Impact

- Affected specs (novas capabilities): `catalog-resolution`, `action-framework`, `scaffold-engine`, `generation-agent`, `forge-cli`.
- Affected code: repositório está vazio hoje — esta mudança cria a estrutura inicial (`cli/`, `domain/`, `agents/`, `actions/`, `engines/`, `catalog/`, `infrastructure/`, `tests/`) conforme layout do RFC.
- Sem breaking changes (não há sistema existente).
