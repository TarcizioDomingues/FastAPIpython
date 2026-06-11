# API de Compras com FastAPI

Projeto desenvolvido para estudo e prática de desenvolvimento de APIs REST utilizando FastAPI.

Ao longo da evolução do projeto foram implementados conceitos importantes do desenvolvimento backend moderno, incluindo persistência em PostgreSQL, migrations com Alembic, Service Layer e autenticação JWT.

## Tecnologias Utilizadas

* Python
* FastAPI
* SQLModel
* PostgreSQL
* Alembic
* Uvicorn
* JWT Authentication
* Git / GitHub

## Funcionalidades

### Compras

* Criar compra
* Listar compras
* Buscar compra por ID
* Atualizar compra
* Remover compra
* Buscar compras por nome do item

### Usuários

* Cadastro de usuário
* Login
* Hash de senha com bcrypt
* Geração de token JWT

## Estrutura do Projeto

```text
app/

├── routers/
│   ├── compras.py
│   └── auth.py
│
├── services/
│   ├── compras_service.py
│   └── auth_service.py
│
├── database.py
├── models.py
├── schemas.py
├── security.py
└── main.py
```

## Arquitetura

O projeto segue uma arquitetura baseada em Service Layer para separar regras de negócio dos endpoints.

```text
Request
   ↓
Router
   ↓
Service
   ↓
Database
   ↓
Response
```

## Banco de Dados

O banco utilizado é o PostgreSQL.

As alterações de estrutura são controladas com Alembic através de migrations versionadas.

Fluxo utilizado:

1. Alterar model
2. Gerar migration
3. Revisar migration
4. Executar upgrade

## Autenticação

A autenticação é baseada em JWT (JSON Web Token).

Fluxo:

```text
Cadastro
   ↓
Hash da senha
   ↓
Login
   ↓
Geração do Token
   ↓
Acesso às rotas protegidas
```

## Como Executar

Instale as dependências:

```bash
pip install -r requirements.txt
```

Configure a conexão com o PostgreSQL.

Execute as migrations:

```bash
alembic upgrade head
```

Inicie a aplicação:

```bash
uvicorn app.main:app --reload
```

A documentação estará disponível em:

```text
http://127.0.0.1:8000/docs
```

## Objetivo do Projeto

Este projeto faz parte da minha jornada de estudos em desenvolvimento backend com Python.

O foco é aprender conceitos utilizados em aplicações reais, evoluindo gradualmente a arquitetura e as boas práticas adotadas no desenvolvimento de APIs.
