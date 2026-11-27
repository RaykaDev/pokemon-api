# 📚 Pokémon API

Este projeto foi desenvolvido para praticar a criação de APIs REST com **FastAPI**, consumo de APIs externas, operações CRUD, persistência de dados com PostgreSQL, testes automatizados e conteinerização com Podman.

**O objetivo:** desenvolver uma API que integra dados da [PokeAPI](https://pokeapi.co/) e permite também cadastrar, consultar, atualizar e excluir Pokémon em um banco de dados próprio.

<br>

## ✨ Sobre o Projeto

A aplicação possui duas funcionalidades principais:

**1. Integração com a PokeAPI**

Consome dados diretamente da API pública utilizando HTTPX, permitindo listar Pokémon com paginação e consultar detalhes individuais. Os dados recebidos são processados e organizados em respostas JSON.

**2. Gerenciamento de Pokémon com PostgreSQL**

Implementa operações CRUD (_Create, Read, Update e Delete_) para gerenciar registros em um banco de dados PostgreSQL. A comunicação com o banco é realizada utilizando SQLAlchemy, enquanto os schemas do Pydantic validam os dados de entrada e saída.

**O sistema também:**

- consome dados externos diretamente da PokeAPI
- lista Pokémon com paginação através dos parâmetros `limit` e `offset`
- retorna informações de paginação, incluindo total de registros, próximo e anterior
- consulta detalhes de Pokémon pelo identificador
- permite cadastrar novos Pokémon no banco de dados
- permite listar e consultar Pokémon armazenados
- permite atualizar e excluir registros
- utiliza PostgreSQL para persistência dos dados
- utiliza SQLAlchemy para mapeamento objeto-relacional (ORM)
- utiliza Pydantic para validação e estruturação dos dados
- trata erros de conexão com a API externa, retornando status code 503
- trata registros não encontrados, retornando status code 404
- utiliza tipagem com type hints
- possui testes automatizados com Pytest e relatório de cobertura com Pytest-Cov
- utiliza Podman e Podman Compose para executar a aplicação e o banco de dados em contêineres

<br>

## 📁 Estrutura de Arquivos

O projeto está organizado de forma modular, separando responsabilidades entre rotas, serviços, modelos, schemas, operações CRUD e testes:

```text
pokemon-api/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   │
│   ├── crud/
│   │   └── pokemon.py
│   │
│   ├── models/
│   │   └── pokemon.py
│   │
│   ├── routes/
│   │   └── pokemon.py
│   │
│   ├── schemas/
│   │   └── pokemon.py
│   │
│   └── services/
│       └── pokeapi.py
│
├── tests/
│   ├── test_pokemon.py
│   └── test_crud.py
│
├── .github/
│   └── workflows/
│       └── ...
│
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── poetry.lock
```

- `app/main.py`: inicializa a aplicação FastAPI e configura o ciclo de vida da aplicação.
- `app/database.py`: configura a conexão com PostgreSQL e disponibiliza sessões do banco.
- `app/crud/pokemon.py`: concentra as operações de criação, consulta, atualização e exclusão.
- `app/models/pokemon.py`: define o modelo ORM e a estrutura da tabela de Pokémon.
- `app/routes/pokemon.py`: define os endpoints da aplicação.
- `app/schemas/pokemon.py`: define os schemas utilizados para validação e resposta dos dados.
- `app/services/pokeapi.py`: realiza as requisições à PokeAPI e processa os dados externos.
- `tests/`: contém os testes automatizados da integração com a PokeAPI e das operações CRUD.
- `Dockerfile`: define as instruções para construir a imagem da aplicação.
- `docker-compose.yml`: configura os serviços da API e do PostgreSQL.
- `.env.example`: disponibiliza um modelo das variáveis de ambiente necessárias.
- `pyproject.toml` e `poetry.lock`: arquivos utilizados pelo Poetry para gerenciamento de dependências.

<br>

## 🛠️ Tecnologias Utilizadas

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge)](https://www.sqlalchemy.org/)
[![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge)](https://docs.pydantic.dev/)
[![HTTPX](https://img.shields.io/badge/HTTPX-333333?style=for-the-badge)](https://www.python-httpx.org/)
[![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![Poetry](https://img.shields.io/badge/Poetry-60A5FA?style=for-the-badge&logo=poetry&logoColor=white)](https://python-poetry.org/)
[![Podman](https://img.shields.io/badge/Podman-892CA0?style=for-the-badge&logo=podman&logoColor=white)](https://podman.io/)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)](https://github.com/features/actions)

<br>

## ▶️ Como Rodar o Projeto

### Pré-requisitos

- Python 3.13 ou superior
- Poetry
- Podman
- Podman Compose

### 1. Clone o repositório

```bash
git clone https://github.com/RaykaDev/pokemon-api
```

### 2. Acesse a pasta do projeto

```bash
cd pokemon-api
```

### 3. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto, utilizando o `.env.example` como referência.

Configure as seguintes variáveis:

```env
DATABASE_URL=postgresql+psycopg://usuario:senha@localhost:5432/pokemon_db
POSTGRES_USER=usuario
POSTGRES_PASSWORD=senha
POSTGRES_DB=pokemon_db
```

Substitua os valores de exemplo pelas credenciais que desejar utilizar.

**Importante:** o arquivo `.env` contém informações privadas e não deve ser enviado ao GitHub.

### 4. Inicie a aplicação e o banco de dados

Com o Podman Machine em execução, utilize:

```bash
podman compose up --build -d
```

O comando constrói a imagem da API e inicia os serviços configurados no `docker-compose.yml`, incluindo o PostgreSQL.

### 5. Verifique os contêineres

```bash
podman compose ps
```

### 6. Acesse a aplicação

**API:**

```text
http://localhost:8000/
```

**Documentação interativa (Swagger UI):**

```text
http://localhost:8000/docs
```

### Comandos úteis do Podman

Visualizar os logs da API:

```bash
podman compose logs api
```

Visualizar os logs do banco de dados:

```bash
podman compose logs db
```

Parar os serviços:

```bash
podman compose down
```

<br>

## 📌 Endpoints

### Integração com a PokeAPI

| Método | Rota                     | Descrição                                  |
| ------ | ------------------------ | ------------------------------------------ |
| `GET`  | `/pokeapi/pokemons`      | Lista Pokémon com paginação                |
| `GET`  | `/pokeapi/pokemons/{id}` | Consulta detalhes de um Pokémon na PokeAPI |

**Exemplos de requisição:**

Listar Pokémon:

```http
GET /pokeapi/pokemons?limit=20&offset=0
```

Consultar Pikachu:

```http
GET /pokeapi/pokemons/25
```

### Gerenciamento de Pokémon — CRUD

| Método   | Rota                     | Descrição                       |
| -------- | ------------------------ | ------------------------------- |
| `POST`   | `/pokemons`              | Cadastra um Pokémon             |
| `GET`    | `/pokemons`              | Lista Pokémon armazenados       |
| `GET`    | `/pokemons/{pokemon_id}` | Consulta um Pokémon pelo ID     |
| `PUT`    | `/pokemons/{pokemon_id}` | Atualiza os dados de um Pokémon |
| `DELETE` | `/pokemons/{pokemon_id}` | Exclui um Pokémon               |

**Exemplo de cadastro:**

```http
POST /pokemons
```

Corpo da requisição:

```json
{
  "nome": "Pikachu",
  "altura": 4,
  "peso": 60,
  "tipo": "Elétrico"
}
```

**Exemplo de resposta:**

```json
{
  "id": 1,
  "nome": "Pikachu",
  "altura": 4,
  "peso": 60,
  "tipo": "Elétrico"
}
```

A documentação Swagger disponibiliza os campos e parâmetros necessários para cada operação.

<br>

## 🧪 Testes

O projeto utiliza **Pytest** para executar testes automatizados, verificando o comportamento dos endpoints, a integração com a PokeAPI, a paginação, o tratamento de erros e as operações CRUD.

Os testes das operações CRUD utilizam um banco SQLite em memória, isolando os testes do banco PostgreSQL utilizado pela aplicação.

### Instalação das dependências

Na raiz do projeto, execute:

```bash
poetry install --with dev --no-root
```

### Executar os testes

```bash
poetry run python -m pytest
```

### Executar os testes com relatório de cobertura

```bash
poetry run python -m pytest --cov=app --cov-report=term-missing
```

O relatório permite visualizar a porcentagem de cobertura dos testes e identificar as linhas de código que ainda não foram executadas.

<br>

## 🐳 Conteinerização

O projeto utiliza **Podman** para construir e executar os contêineres da aplicação e do banco de dados.

O `Dockerfile` define a imagem da API, enquanto o `docker-compose.yml` configura os serviços e a comunicação entre eles.

**Construir e iniciar os serviços:**

```bash
podman compose up --build -d
```

**Verificar os contêineres:**

```bash
podman compose ps
```

**Visualizar os logs:**

```bash
podman compose logs
```

**Parar os serviços:**

```bash
podman compose down
```

Os dados do PostgreSQL são persistidos em um volume, permitindo que continuem disponíveis após a parada e recriação dos contêineres.

<br>

## ⚙️ Integração Contínua (CI)

O projeto utiliza **GitHub Actions** para automatizar a execução dos testes durante o fluxo de desenvolvimento.

A integração contínua permite verificar se as alterações realizadas mantêm o funcionamento esperado da aplicação antes de serem incorporadas à branch principal.

<br>

## 🚀 Deploy

**API em produção:** https://pokemon-api-p7nt.vercel.app/

**Documentação Swagger:** https://pokemon-api-p7nt.vercel.app/docs

A aplicação possui uma versão publicada na Vercel.

Para disponibilizar todas as funcionalidades da versão atual em produção, é necessário configurar um serviço PostgreSQL externo e definir a variável `DATABASE_URL` nas configurações de ambiente da hospedagem.

<br>

## 📌 Aprendizados

- Criação e organização de APIs REST com FastAPI
- Estruturação modular de aplicações Python
- Separação de responsabilidades entre rotas, serviços, modelos, schemas e operações CRUD
- Consumo de APIs externas utilizando HTTPX
- Realização de requisições HTTP e tratamento de respostas
- Manipulação e transformação de dados JSON
- Implementação de paginação com `limit` e `offset`
- Criação de operações CRUD
- Persistência de dados com PostgreSQL
- Mapeamento objeto-relacional com SQLAlchemy
- Validação de dados com Pydantic
- Gerenciamento de sessões e conexões com banco de dados
- Tratamento de exceções e erros HTTP
- Criação de testes automatizados com Pytest
- Isolamento de testes com SQLite em memória
- Simulação de falhas externas com `monkeypatch`
- Análise de cobertura com Pytest-Cov
- Gerenciamento de dependências com Poetry
- Construção e execução de contêineres com Podman
- Orquestração de serviços com Podman Compose
- Integração contínua com GitHub Actions
- Documentação automática com Swagger UI
