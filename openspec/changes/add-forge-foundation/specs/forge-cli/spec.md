## ADDED Requirements

### Requirement: Comando de Criação Interativo
O comando `forge create`, executado sem flags, SHALL apresentar ao usuário uma lista dos Blueprints disponíveis no catálogo para seleção única, seguida de uma lista dos Components disponíveis para seleção múltipla, e então invocar o `BlueprintAgent` com as escolhas feitas.

#### Scenario: Usuário completa fluxo interativo
- **WHEN** o usuário executa `forge create` e seleciona um Blueprint e um ou mais Components válidos
- **THEN** a CLI invoca o `BlueprintAgent` com o Blueprint e a lista de Components selecionados

#### Scenario: Catálogo de blueprints vazio
- **WHEN** o usuário executa `forge create` e não há nenhum Blueprint em `catalog/blueprints/`
- **THEN** a CLI informa que não há Blueprints disponíveis e encerra sem iniciar o modo interativo de seleção de Components

### Requirement: Comando de Criação Não Interativo
O comando `forge create --blueprint <nome> --name <projeto> --components <csv>` SHALL executar a geração sem prompts, usando os valores fornecidos via flags, e SHALL suportar `--components` vazio ou omitido (gerando o projeto apenas com o Blueprint).

#### Scenario: Criação não interativa com components
- **WHEN** o usuário executa `forge create --blueprint cloud-run --name payments-api --components bigquery,secret-manager`
- **THEN** a CLI invoca o `BlueprintAgent` diretamente com esses valores, sem exibir prompts

#### Scenario: Criação não interativa sem components
- **WHEN** o usuário executa `forge create --blueprint python-library --name meu-lib` sem informar `--components`
- **THEN** a CLI invoca o `BlueprintAgent` com lista de Components vazia

### Requirement: Validação de Entrada Antes da Geração
A CLI SHALL validar que o Blueprint informado (via flag ou seleção interativa) existe no catálogo antes de invocar o `BlueprintAgent`, exibindo mensagem de erro acionável e código de saída não-zero em caso de nome inválido.

#### Scenario: Blueprint inexistente via flag
- **WHEN** o usuário executa `forge create --blueprint inexistente --name x`
- **THEN** a CLI exibe erro informando que o Blueprint `inexistente` não foi encontrado no catálogo e encerra com código de saída não-zero, sem invocar o `BlueprintAgent`
