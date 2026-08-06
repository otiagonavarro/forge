<!-- markdownlint-disable -->
## 1. Estrutura Base do Repositório

- [x] 1.1 Criar `pyproject.toml` (Python >=3.11) com dependências iniciais (`cookiecutter`, `pyyaml`, `click` ou `typer` para CLI)
- [x] 1.2 Criar diretórios `cli/`, `domain/`, `agents/`, `actions/`, `engines/`, `catalog/{blueprints,components}/`, `infrastructure/`, `tests/`, `docs/` conforme layout do RFC
- [x] 1.3 Configurar lint/format (ex.: ruff) e runner de testes (pytest)

## 2. Catalog Resolution

- [x] 2.1 Definir dataclasses/schema para manifesto de Blueprint (`name`, `version`, `engine`) e Component (`name`, `version`, `dependencies`, `variables`, `files`, `hooks`, `depends_on`)
- [x] 2.2 Implementar `BlueprintResolver` (carregar + validar `blueprint.yaml`, erro se Blueprint não existe ou manifesto ausente)
- [x] 2.3 Implementar `ComponentResolver` (carregar Components, expandir `depends_on` transitivamente, ordenação topológica, detecção de ciclo, erro se Component não existe)
- [x] 2.4 Criar fixtures de teste em `tests/fixtures/catalog/` (>=1 blueprint fake, >=3 components fake com pelo menos uma cadeia de `depends_on` e um ciclo forçado para teste negativo)
- [x] 2.5 Testes unitários cobrindo todos os cenários de `specs/catalog-resolution/spec.md`

## 3. Scaffold Engine

- [x] 3.1 Definir interface `ScaffoldEngine` (`render(template_path, destination, context)`)
- [x] 3.2 Implementar registro de engines por nome (dict simples, sem plugin system)
- [x] 3.3 Implementar `CookiecutterEngine` sobre a lib `cookiecutter`
- [x] 3.4 Testes cobrindo seleção de engine registrada/não registrada e renderização via Cookiecutter

## 4. Action Framework

- [x] 4.1 Definir contrato base `Action.execute(context)` e classe `GenerationContext` (diretório destino, blueprint resolvido, components resolvidos ordenados, variáveis)
- [x] 4.2 Implementar `CreateDirectory` (com validação de diretório não vazio)
- [x] 4.3 Implementar `RenderBlueprint` (delega à Scaffold Engine do manifesto)
- [x] 4.4 Implementar `InstallComponent` (copia arquivos/templates, executa `after_install` hook quando existir, propaga erro por Component)
- [x] 4.5 Implementar `InitializeGit` (`git init` local, sem commit/push automático)
- [x] 4.6 Implementar `ValidateProject` (checa estrutura mínima do Blueprint + Components instalados)
- [x] 4.7 Testes cobrindo todos os cenários de `specs/action-framework/spec.md`

## 5. Generation Agent

- [x] 5.1 Implementar `BlueprintAgent` orquestrando resolução (Blueprint + Components) e execução das Actions na ordem definida
- [x] 5.2 Implementar tratamento de erro: interrupção no primeiro passo que falhar, mensagem identificando a Action, sem rollback automático
- [x] 5.3 Testes de integração cobrindo pipeline completo com fixtures (sucesso, falha de resolução, falha de Action intermediária)

## 6. Forge CLI

- [x] 6.1 Implementar comando `forge create` interativo (lista blueprints → seleção única; lista components → seleção múltipla)
- [x] 6.2 Implementar modo não interativo (`--blueprint`, `--name`, `--components`)
- [x] 6.3 Implementar validação de entrada (Blueprint/Components inexistentes) com mensagem acionável e exit code não-zero
- [x] 6.4 Testes de CLI (interativo simulado + não interativo) cobrindo `specs/forge-cli/spec.md`

## 7. Validação Final

- [x] 7.1 Rodar suíte de testes completa (`pytest`)
- [x] 7.2 `openspec validate add-forge-foundation --strict`
- [x] 7.3 Atualizar `openspec/project.md` com stack (Python, Cookiecutter) e convenções definidas nesta mudança
