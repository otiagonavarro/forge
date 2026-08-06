## ADDED Requirements

### Requirement: Estrutura de Catálogo
O sistema SHALL organizar o catálogo em `catalog/blueprints/<nome>/` e `catalog/components/<nome>/`, onde cada Blueprint contém um manifesto `blueprint.yaml` e seus templates, e cada Component contém `component.yaml`, diretório `templates/`, `hooks.py` opcional e `README.md`.

#### Scenario: Blueprint sem manifesto é inválido
- **WHEN** um diretório existe em `catalog/blueprints/<nome>/` sem `blueprint.yaml`
- **THEN** a resolução desse Blueprint falha com erro indicando manifesto ausente

#### Scenario: Component sem manifesto é inválido
- **WHEN** um diretório existe em `catalog/components/<nome>/` sem `component.yaml`
- **THEN** a resolução desse Component falha com erro indicando manifesto ausente

### Requirement: Schema de Manifesto de Blueprint
O manifesto `blueprint.yaml` SHALL declarar `name`, `version` e `engine` (nome da Scaffold Engine a ser usada para renderizar o Blueprint).

#### Scenario: Manifesto de Blueprint válido é carregado
- **WHEN** `blueprint.yaml` contém `name`, `version` e `engine` válidos
- **THEN** o BlueprintResolver carrega o Blueprint com esses metadados disponíveis para as Actions

#### Scenario: Engine desconhecida no manifesto
- **WHEN** `blueprint.yaml` declara um `engine` não registrado na Scaffold Engine
- **THEN** a resolução falha com erro explícito citando o nome da engine desconhecida

### Requirement: Schema de Manifesto de Component
O manifesto `component.yaml` SHALL declarar `name`, `version`, `dependencies` (lista de pacotes), `variables`, `files` e, opcionalmente, `hooks` (ex.: `after_install`) e `depends_on` (lista de nomes de outros Components).

#### Scenario: Manifesto de Component válido é carregado
- **WHEN** `component.yaml` contém `name` e `version`
- **THEN** o ComponentResolver carrega o Component com `dependencies`, `variables`, `files`, `hooks` e `depends_on` disponíveis (usando default vazio para campos opcionais ausentes)

### Requirement: Resolução de Blueprint
O BlueprintResolver SHALL, dado um nome de Blueprint, localizar e validar seu manifesto no catálogo, retornando erro claro se o Blueprint não existir.

#### Scenario: Blueprint inexistente
- **WHEN** o usuário solicita um Blueprint cujo nome não existe em `catalog/blueprints/`
- **THEN** o sistema retorna erro informando que o Blueprint não foi encontrado, sem iniciar geração

### Requirement: Resolução de Components com Dependências
O ComponentResolver SHALL, dada uma lista de Components solicitados, expandir transitivamente `depends_on`, detectar ciclos e produzir uma lista final ordenada topologicamente (dependências antes de quem depende delas), falhando com erro claro em caso de Component inexistente ou ciclo de dependência.

#### Scenario: Component inexistente na solicitação
- **WHEN** o usuário solicita um Component cujo nome não existe em `catalog/components/`
- **THEN** o sistema retorna erro informando qual Component não foi encontrado, sem iniciar geração

#### Scenario: Dependência transitiva é incluída automaticamente
- **WHEN** o Component `A` solicitado declara `depends_on: [B]` e `B` não foi solicitado explicitamente
- **THEN** o ComponentResolver inclui `B` na lista final, ordenado antes de `A`

#### Scenario: Ciclo de dependência é rejeitado
- **WHEN** o Component `A` depende de `B` e `B` depende de `A` (direta ou transitivamente)
- **THEN** o ComponentResolver falha com erro indicando o ciclo detectado, sem produzir lista parcial
