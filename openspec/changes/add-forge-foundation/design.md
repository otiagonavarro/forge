<!-- markdownlint-disable -->
## Context

Repositório `forge` está vazio (sem código). RFC-0001 define visão completa da plataforma (Blueprints, Components, Agents, Actions, Scaffold Engine) mas o roadmap do próprio RFC separa **Foundation** das camadas de conteúdo (Blueprints, Components). Esta mudança materializa só a Foundation, para permitir revisão/validação da arquitetura antes de investir em blueprints/components reais.

## Goals / Non-Goals

- Goals:
  - Estabelecer os 5 contratos centrais (`Action`, `ScaffoldEngine`, `BlueprintResolver`/`ComponentResolver`, `BlueprintAgent`, CLI) rodáveis ponta a ponta com fixtures de teste.
  - Manter Blueprints/Components como dados de catálogo plugáveis, sem lógica de negócio hardcoded na engine.
  - Layout de repositório e linguagem alinhados ao RFC (Python, `pyproject.toml`, Cookiecutter como primeira engine).
- Non-Goals:
  - Publicar blueprints/components reais no catálogo.
  - Implementar Copier ou Native Engine.
  - Deploy, CI/CD, Terraform apply — Forge só gera arquivos (não objetivo do RFC).

## Decisions

- **Decision**: linguagem Python (>=3.11), gerenciado via `pyproject.toml`, conforme exemplos de código do RFC.
  - Alternativas: Go/TS — descartadas por não haver exemplo/precedente no RFC e por Cookiecutter ser nativo Python.
- **Decision**: catálogo (`catalog/blueprints`, `catalog/components`) começa vazio nesta mudança; testes de integração usam fixtures em `tests/fixtures/catalog/` para validar o pipeline completo sem acoplar Foundation a um blueprint real.
  - Alternativa considerada: incluir um blueprint mínimo real (ex.: `python-library`) no catálogo já nesta mudança — descartada para manter o escopo estritamente "Foundation", deixando a decisão de qual blueprint entra primeiro para a próxima mudança.
- **Decision**: `ComponentResolver` resolve `depends_on` com ordenação topológica e falha com erro explícito em ciclo ou componente inexistente. Necessário mesmo sem components reais, pois é contrato de domínio testável com fixtures.
- **Decision**: `BlueprintAgent` não faz rollback automático em falha de Action — mantém o diretório parcialmente gerado e reporta claramente qual Action falhou e em que passo do pipeline. Forge não gerencia estado/deploy (não objetivo do RFC), então rollback automático adicionaria complexidade sem benefício claro nesta fase; usuário decide se descarta o diretório.
- **Decision**: `ScaffoldEngine` é selecionado por nome declarado no manifesto do blueprint (`engine: cookiecutter`), resolvido via registry simples (dict). Suporta adicionar Copier/Native depois sem mudar `BlueprintAgent`/Actions.

## Risks / Trade-offs

- Sem blueprint real no catálogo, o valor entregue ao usuário final desta mudança é só infraestrutura — mitigado por deixar isso explícito no proposal e já planejar a próxima mudança (ex.: `add-blueprint-cloud-run`) em seguida.
- Ausência de rollback automático pode deixar diretórios parciais após falha — mitigado exigindo que `ValidateProject` e mensagens de erro do `BlueprintAgent` deixem claro o estado e o passo que falhou.

## Migration Plan

N/A — projeto novo, sem usuários/dados existentes.

## Open Questions

- Qual o primeiro blueprint real a ser implementado após a Foundation (Cloud Run é o candidato natural pelo RFC, mas não foi confirmado)?
- Componentes vão precisar de versionamento semântico com resolução de conflito de `dependencies` (pip) entre múltiplos components instalados na mesma pipeline? Não tratado nesta mudança por não haver components reais ainda.
