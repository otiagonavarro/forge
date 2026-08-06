## ADDED Requirements

### Requirement: Orquestração pelo BlueprintAgent
O `BlueprintAgent` SHALL orquestrar o fluxo completo de geração: interpretar a entrada do usuário, resolver o Blueprint, resolver os Components (com dependências), executar as Actions `CreateDirectory`, `RenderBlueprint`, `InstallComponent`, `InitializeGit` e `ValidateProject` nessa ordem, e retornar um resultado indicando sucesso ou falha.

#### Scenario: Pipeline completo bem-sucedido
- **WHEN** o usuário solicita um Blueprint e Components válidos e existentes no catálogo
- **THEN** o `BlueprintAgent` executa as Actions na ordem definida e retorna sucesso com o caminho do projeto gerado

### Requirement: Agents Não Manipulam Arquivos Diretamente
O `BlueprintAgent` SHALL delegar toda manipulação de arquivos e sistema a Actions; ele NÃO SHALL ler, escrever ou renderizar arquivos diretamente.

#### Scenario: Falha de resolução não gera nenhum arquivo
- **WHEN** a resolução de Blueprint ou de Components falha
- **THEN** nenhuma Action de manipulação de arquivos é executada e nenhum diretório de projeto é criado

### Requirement: Tratamento de Erro no Pipeline
Se qualquer Action falhar durante a execução, o `BlueprintAgent` SHALL interromper o pipeline imediatamente, reportar claramente qual Action falhou e o motivo, e preservar o estado parcial gerado até aquele ponto (sem rollback automático).

#### Scenario: Falha em Action intermediária interrompe o pipeline
- **WHEN** a Action `InstallComponent` falha durante a instalação de um Component
- **THEN** o `BlueprintAgent` não executa `InitializeGit` nem `ValidateProject`, e retorna erro identificando `InstallComponent` como a etapa que falhou

#### Scenario: Estado parcial é preservado após falha
- **WHEN** o pipeline falha após `RenderBlueprint` já ter gerado arquivos
- **THEN** os arquivos já gerados permanecem no diretório do projeto para inspeção, e o resultado retornado indica claramente que a geração não foi concluída
