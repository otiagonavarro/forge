## ADDED Requirements

### Requirement: Abstração ScaffoldEngine
O sistema SHALL expor uma interface `ScaffoldEngine` com o método `render(template_path, destination, context)`, permitindo múltiplas implementações de geração de arquivos sem alterar Actions, Agents ou CLI.

#### Scenario: Nova engine implementa a interface
- **WHEN** uma nova implementação de `ScaffoldEngine` é adicionada
- **THEN** ela implementa `render(template_path, destination, context)` e pode ser usada por `RenderBlueprint` sem alterações no restante do pipeline

### Requirement: Registro e Seleção de Engine por Nome
O sistema SHALL manter um registro de engines disponíveis por nome (ex.: `cookiecutter`), usado para resolver a engine declarada no manifesto do Blueprint em tempo de geração.

#### Scenario: Engine registrada é selecionada corretamente
- **WHEN** um Blueprint declara `engine: cookiecutter`
- **THEN** o sistema resolve e usa a instância de `CookiecutterEngine` registrada sob esse nome

#### Scenario: Engine não registrada
- **WHEN** um Blueprint declara um nome de engine que não está no registro
- **THEN** o sistema falha antes de iniciar a renderização, com erro citando o nome da engine ausente

### Requirement: Implementação CookiecutterEngine
O sistema SHALL fornecer `CookiecutterEngine`, uma implementação de `ScaffoldEngine` que renderiza templates usando a biblioteca Cookiecutter, traduzindo as variáveis do contexto Forge para o formato de contexto esperado pelo Cookiecutter.

#### Scenario: Renderização via Cookiecutter
- **WHEN** `CookiecutterEngine.render(...)` é chamado com um diretório de template compatível com Cookiecutter e variáveis de contexto
- **THEN** os arquivos resultantes são gerados no diretório destino com as variáveis substituídas
