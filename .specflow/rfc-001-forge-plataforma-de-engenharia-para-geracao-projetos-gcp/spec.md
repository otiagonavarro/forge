<!-- markdownlint-disable -->
# RFC-0001 - Forge: Plataforma de Engenharia para Geração de Projetos GCP

| Status | Draft |
| -------- | ------- |
| Autor | Tiago Navarro |
| Data | 2026-07-26 |
| Versão | 1.0 |

---

# Resumo

Este RFC propõe a criação do **Forge**, uma plataforma de engenharia responsável por padronizar a criação de projetos que utilizam serviços do Google Cloud Platform (GCP).

Diferentemente de um simples gerador de templates, o Forge será uma plataforma capaz de gerar projetos completos a partir de **Blueprints Arquiteturais** e **Components**, orquestrados por **Agents** e executados através de um conjunto de **Actions**.

A plataforma deverá abstrair a complexidade da criação de novos serviços, reduzindo esforço operacional, aumentando a padronização e permitindo que novos padrões arquiteturais sejam disseminados automaticamente para toda a organização.

O Forge deverá ser independente da tecnologia utilizada para geração de código, permitindo a utilização de ferramentas como Cookiecutter, Copier ou uma implementação própria.

---

# Motivação

Ao longo do crescimento da plataforma de dados e engenharia, novos projetos são criados constantemente.

Alguns exemplos:

- Cloud Run
- Cloud Functions
- Cloud Run Jobs
- Vertex AI Agents
- Dataflow
- Dataproc
- APIs internas
- Bibliotecas Python
- Terraform Modules
- Workers
- Serviços Pub/Sub

Embora possuam responsabilidades diferentes, praticamente todos compartilham uma grande quantidade de configurações comuns.

Entre elas:

- Docker
- Estrutura do projeto
- Logging
- Observabilidade
- Secret Manager
- IAM
- Terraform
- Cloud Build
- GitHub Actions
- Testes
- Configuração de ambientes
- Health Check
- Padronização arquitetural

Hoje essas configurações são copiadas manualmente entre projetos, causando:

- duplicação de código;
- inconsistência entre serviços;
- dificuldade para evoluir padrões;
- maior tempo para bootstrap de novos projetos;
- maior custo de manutenção.

O Forge busca resolver esse problema centralizando toda essa inteligência em uma plataforma única.

---

# Objetivos

O Forge deverá permitir:

- gerar qualquer tipo de projeto baseado em GCP;
- padronizar arquitetura entre serviços;
- reutilizar componentes;
- reduzir o tempo de bootstrap;
- centralizar boas práticas;
- desacoplar templates da lógica de geração;
- facilitar evolução da plataforma;
- reduzir custo de manutenção.

---

# Não Objetivos

O Forge não tem como objetivo:

- realizar deploy;
- substituir Terraform;
- substituir CI/CD;
- substituir frameworks de desenvolvimento;
- substituir bibliotecas internas.

Seu objetivo é exclusivamente gerar projetos padronizados.

---

# Visão Geral

```text
                     Usuário

                        │

                        ▼

                  Forge CLI

                        │

                        ▼

                Blueprint Agent

                        │

          ┌─────────────┴─────────────┐

          ▼                           ▼

   Blueprint Resolver         Component Resolver

          │                           │

          └─────────────┬─────────────┘

                        ▼

                    Actions

                        ▼

                Scaffold Engine

                        ▼

       Cookiecutter / Copier / Native

                        ▼

                Projeto Gerado
```

---

# Arquitetura

O Forge será dividido em cinco conceitos principais.

## Blueprints

Blueprints representam um tipo de projeto.

Eles definem apenas a estrutura mínima necessária para determinado serviço.

Exemplos:

- Cloud Run
- Cloud Function
- Cloud Run Job
- Dataflow
- Dataproc
- Vertex AI Agent
- Terraform Module
- Python Library

Um Blueprint não contém funcionalidades específicas.

Ele define apenas:

- estrutura;
- runtime;
- pipeline;
- organização de diretórios;
- arquivos mínimos.

Exemplo:

```text
Blueprint Cloud Run

src/

tests/

Dockerfile

README

pyproject.toml

cloudbuild.yaml
```

---

## Components

Components representam funcionalidades reutilizáveis que podem ser adicionadas a qualquer Blueprint.

Exemplos:

- BigQuery
- Cloud Storage
- Pub/Sub
- Secret Manager
- Firestore
- Logging
- OpenTelemetry
- Cloud Scheduler
- Redis
- Postgres
- Vertex AI
- Authentication
- Health Check
- OpenAPI
- gRPC

Cada componente pode adicionar:

- código;
- dependências;
- configurações;
- arquivos;
- documentação;
- hooks.

---

## Agents

Agents representam fluxos completos de geração.

Eles possuem responsabilidade exclusivamente de orquestração.

Exemplos:

```text
CloudRunAgent

CloudFunctionAgent

DataflowAgent

VertexAgent

MigrationAgent
```

Responsabilidades:

- interpretar entrada do usuário;
- selecionar Blueprint;
- resolver Components;
- executar Actions;
- validar resultado.

Os Agents não manipulam arquivos diretamente.

---

## Actions

Actions representam operações pequenas e reutilizáveis.

Cada Action possui uma única responsabilidade.

Exemplos:

```text
RenderBlueprint

InstallComponent

CreateDirectory

UpdatePyProject

UpdateDockerfile

UpdateTerraform

InitializeGit

ValidateProject
```

Todas seguem um contrato semelhante:

```python
class Action:

    def execute(context):
        ...
```

---

## Scaffold Engine

O Forge não dependerá diretamente de nenhuma ferramenta de geração.

Será criada uma abstração.

```python
class ScaffoldEngine:

    def render(...)
```

Implementações possíveis:

- Cookiecutter
- Copier
- Native Engine

Isso permite substituir o mecanismo de geração sem alterar o restante da arquitetura.

---

# Estrutura do Repositório

```text
forge/

├── agents/
│
├── actions/
│
├── engines/
│   ├── cookiecutter_engine.py
│   ├── copier_engine.py
│   └── native_engine.py
│
├── catalog/
│   │
│   ├── blueprints/
│   │
│   │   ├── cloud-run/
│   │   ├── cloud-function/
│   │   ├── cloud-run-job/
│   │   ├── dataproc/
│   │   ├── dataflow/
│   │   ├── vertex-agent/
│   │   ├── python-library/
│   │   └── terraform-module/
│   │
│   └── components/
│       │
│       ├── bigquery/
│       ├── cloud-storage/
│       ├── firestore/
│       ├── pubsub/
│       ├── logging/
│       ├── tracing/
│       ├── metrics/
│       ├── opentelemetry/
│       ├── scheduler/
│       ├── secret-manager/
│       ├── auth/
│       ├── grpc/
│       ├── openapi/
│       ├── postgres/
│       ├── redis/
│       ├── vertex-ai/
│       └── healthcheck/
│
├── cli/
│
├── domain/
│
├── infrastructure/
│
├── tests/
│
└── docs/
```

---

# Estrutura de um Component

Cada componente deverá ser autocontido.

```text
components/

bigquery/

component.yaml

templates/

hooks.py

README.md
```

Exemplo de manifesto:

```yaml
name: bigquery

version: 1.0

dependencies:
  - google-cloud-bigquery

variables:
  - GCP_PROJECT_ID

files:
  - templates/bigquery_client.py

hooks:
  after_install: hooks.after_install
```

---

# Fluxo de Geração

```text
Usuário

↓

Forge CLI

↓

Seleciona Blueprint

↓

Seleciona Components

↓

Blueprint Agent

↓

Resolver Components

↓

Render Blueprint

↓

Instalar Components

↓

Executar Hooks

↓

Validar Projeto

↓

Projeto Final
```

---

# Interface da CLI

Modo interativo:

```bash
forge create
```

Exemplo:

```text
Qual Blueprint deseja utilizar?

Cloud Run

Cloud Function

Cloud Run Job

Dataflow

Dataproc

Vertex AI Agent

Python Library

Terraform Module
```

Depois:

```text
Quais Components deseja instalar?

✓ BigQuery

✓ Secret Manager

✓ Pub/Sub

✓ Logging

✓ OpenTelemetry

✓ Health Check
```

Modo não interativo:

```bash
forge create \
    --blueprint cloud-run \
    --name payments-api \
    --components bigquery,pubsub,secret-manager,logging
```

---

# Exemplo

Entrada:

```text
Blueprint

Cloud Run

Components

BigQuery

Pub/Sub

Secret Manager

Logging
```

Resultado:

```text
payments-api/

src/

tests/

Dockerfile

README.md

terraform/

.github/

cloudbuild.yaml

pyproject.toml
```

Com:

- cliente BigQuery;
- cliente Pub/Sub;
- cliente Secret Manager;
- logging estruturado;
- health check;
- Docker;
- pipeline;
- testes.

---

# Evolução dos Blueprints

Blueprints deverão permanecer pequenos.

Eles representam apenas a estrutura mínima.

Toda funcionalidade adicional deverá ser implementada através de Components.

---

# Evolução dos Components

Components deverão ser independentes.

Dependências entre Components deverão ser explícitas.

Exemplo:

```yaml
depends_on:

logging

secret-manager
```

---

# Roadmap

## Foundation

- CLI
- Domain
- Agents
- Actions
- Scaffold Engine
- Cookiecutter Engine

---

## Blueprints

- Cloud Run
- Cloud Function
- Cloud Run Job
- Python Library
- Terraform Module

---

## Data Platform

- Dataflow
- Dataproc
- Pub/Sub Worker

---

## AI Platform

- Vertex AI Agent
- Agent Development Kit
- MCP Server

---

## Components

- BigQuery
- Firestore
- Pub/Sub
- Secret Manager
- Cloud Storage
- Logging
- OpenTelemetry
- Scheduler
- Redis
- Postgres
- Authentication

---

## Platform

- GitHub Actions
- Cloud Build
- Terraform
- Artifact Registry
- IAM

---

## Marketplace

Adicionar um catálogo interno de Blueprints e Components.

Exemplo:

```bash
forge search

forge install

forge update
```

---

# Futuras Evoluções

A arquitetura permitirá expansão para outros tipos de projetos.

Exemplos:

- APIs REST
- Workers
- Airflow DAGs
- Data Pipelines
- CLI Applications
- Eventarc
- Batch Jobs
- Vertex Extensions
- Gemini Agents
- MCP Servers
- Bibliotecas compartilhadas

---

# Benefícios Esperados

## Engenharia

- menor tempo para criação de projetos;
- padronização da arquitetura;
- menor curva de aprendizado;
- redução de código duplicado.

## Plataforma

- evolução centralizada;
- propagação automática de boas práticas;
- redução do custo de manutenção;
- maior consistência entre serviços.

## Arquitetura

- separação clara de responsabilidades;
- baixo acoplamento;
- alta extensibilidade;
- independência da ferramenta de scaffolding.

---

# Princípios Arquiteturais

O Forge será guiado pelos seguintes princípios:

- **Blueprints definem a estrutura** de um projeto.
- **Components adicionam capacidades** reutilizáveis.
- **Agents orquestram** o fluxo de geração.
- **Actions executam operações** específicas e reutilizáveis.
- **Scaffold Engines materializam** o projeto utilizando uma tecnologia de geração desacoplada da lógica de negócio.

Essa separação permite que cada camada evolua independentemente, reduzindo acoplamento e facilitando a manutenção da plataforma.

---

# Considerações Finais

O Forge não deve ser encarado como um simples repositório de templates, mas como uma plataforma de engenharia para padronização do desenvolvimento em GCP.

Sua arquitetura é baseada em quatro pilares:

- **Blueprints**, que representam padrões arquiteturais de projetos.
- **Components**, que encapsulam capacidades reutilizáveis.
- **Agents**, que coordenam a geração de projetos.
- **Actions**, que executam as operações necessárias para construir o projeto.

Com a abstração da camada de geração por meio de um **Scaffold Engine**, o Forge permanece independente de ferramentas específicas, permitindo a adoção de novas tecnologias de scaffolding no futuro sem impacto sobre a arquitetura principal.

Essa abordagem cria uma base sólida para evolução da plataforma de engenharia, promovendo consistência, reutilização e escalabilidade na criação de qualquer projeto baseado em Google Cloud Platform.
