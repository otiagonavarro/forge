## ADDED Requirements

### Requirement: Contrato de Action
Toda Action SHALL implementar `execute(context)`, onde `context` carrega o estado da geração em curso (diretório destino, Blueprint resolvido, lista ordenada de Components resolvidos, variáveis). Uma Action SHALL ter responsabilidade única e não SHALL orquestrar outras Actions.

#### Scenario: Action expõe execute(context)
- **WHEN** uma nova Action é registrada no pipeline de geração
- **THEN** ela implementa o método `execute(context)` e não invoca diretamente outra Action

### Requirement: CreateDirectory Action
A Action `CreateDirectory` SHALL criar o diretório do projeto no caminho definido pelo contexto, falhando com erro claro se o diretório já existir e não estiver vazio.

#### Scenario: Diretório destino já existe e não está vazio
- **WHEN** `CreateDirectory` executa e o diretório destino já existe com arquivos
- **THEN** a Action falha com erro explícito, sem sobrescrever conteúdo existente

### Requirement: RenderBlueprint Action
A Action `RenderBlueprint` SHALL invocar a Scaffold Engine declarada no manifesto do Blueprint resolvido para renderizar os templates do Blueprint no diretório do projeto.

#### Scenario: Blueprint é renderizado com a engine declarada
- **WHEN** `RenderBlueprint` executa com um Blueprint cujo manifesto declara `engine: cookiecutter`
- **THEN** a Action delega a renderização à `CookiecutterEngine` passando o caminho de templates do Blueprint e as variáveis do contexto

### Requirement: InstallComponent Action
A Action `InstallComponent` SHALL, para cada Component na lista ordenada resolvida, copiar seus `files`/`templates` para o diretório do projeto e executar o hook `after_install` quando declarado.

#### Scenario: Component sem hook after_install
- **WHEN** um Component resolvido não declara `hooks.after_install`
- **THEN** `InstallComponent` copia seus arquivos normalmente e não tenta executar hook

#### Scenario: Hook after_install falha
- **WHEN** o hook `after_install` de um Component lança exceção
- **THEN** `InstallComponent` interrompe a instalação dos Components restantes e propaga o erro identificando qual Component falhou

### Requirement: InitializeGit Action
A Action `InitializeGit` SHALL inicializar um repositório git no diretório do projeto gerado (`git init`), sem realizar commit automático de push para remoto algum.

#### Scenario: Repositório git é inicializado
- **WHEN** `InitializeGit` executa após o diretório do projeto estar populado
- **THEN** um repositório `.git` é criado localmente no diretório do projeto

### Requirement: ValidateProject Action
A Action `ValidateProject` SHALL verificar, ao final do pipeline, que a estrutura mínima do Blueprint foi gerada e que todos os Components solicitados foram instalados, reportando erro claro caso algo esperado esteja ausente.

#### Scenario: Estrutura mínima ausente
- **WHEN** `ValidateProject` executa e um arquivo/diretório declarado como obrigatório pelo Blueprint não existe no projeto gerado
- **THEN** a Action falha reportando qual item esperado está ausente
