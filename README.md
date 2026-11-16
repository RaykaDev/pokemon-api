# 📚 Pokémon API

Este é um projeto desenvolvido para praticar a criação de APIs REST com **FastAPI**, consumo de APIs externas, organização modular de aplicações back-end, testes automatizados e conteinerização com Podman.

**O objetivo é simples:** desenvolver uma API que consome dados diretamente da [PokeAPI](https://pokeapi.co/), permitindo listar Pokémon de forma paginada e consultar os detalhes de um Pokémon específico.

<br>

## ✨ Sobre o Projeto

Neste sistema, os dados dos Pokémon são obtidos diretamente da **PokeAPI**, uma API pública que disponibiliza informações sobre os Pokémon. A aplicação utiliza a biblioteca **HTTPX** para realizar as requisições HTTP e processar os dados recebidos.

A API disponibiliza dois endpoints principais: um para listar Pokémon com paginação, permitindo controlar a quantidade de resultados e o deslocamento inicial (`limit` e `offset`), e outro para consultar os detalhes de um Pokémon específico pelo seu `id`.

As respostas são organizadas em um formato JSON próprio, contendo informações como nome, identificador, altura, tipos e sprites (imagens frontal e traseira). A documentação interativa é disponibilizada automaticamente pelo FastAPI através do Swagger UI (`/docs`).

**O sistema também:**

- consome dados diretamente da PokeAPI, sem depender de armazenamento local
- lista Pokémon com paginação através dos parâmetros `limit` e `offset`
- retorna informações de paginação, incluindo total de registros, próximo e anterior
- consulta os detalhes de um Pokémon específico pelo seu identificador
- organiza os dados recebidos da API externa em um formato JSON padronizado
- utiliza HTTPX para realizar requisições HTTP com configuração de timeout
- trata erros de conexão com a API externa, retornando status code 503
- trata Pokémon não encontrados, retornando status code 404
- valida os parâmetros de paginação, impedindo valores inválidos
- utiliza tipagem com type hints nas funções
- possui testes automatizados com Pytest e relatório de cobertura com Pytest-Cov
- utiliza Podman para construir e executar a aplicação em contêiner

<br>

## 📁 Estrutura de Arquivos

O projeto está organizado de forma modular, separando a aplicação, as rotas, os serviços e os testes:

```text
pokemon-api/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   └── pokemon.py
│   │
│   └── services/
│       ├── __init__.py
│       └── pokeapi.py
│
├── tests/
│   └── test_pokemon.py
│
├── Dockerfile
├── .dockerignore
├── .gitignore
├── pyproject.toml
└── poetry.lock
```

- `app/main.py`: inicializa a aplicação FastAPI e registra as rotas.
- `app/routes/pokemon.py`: define os endpoints de consulta dos Pokémon.
- `app/services/pokeapi.py`: realiza as requisições à PokeAPI, processa os dados e trata os erros.
- `tests/test_pokemon.py`: contém os testes automatizados dos endpoints e dos comportamentos da aplicação.
- `Dockerfile`: define as instruções para construir a imagem da aplicação.
- `.dockerignore`: especifica os arquivos e diretórios que não devem ser enviados durante a construção da imagem.
- `.gitignore`: especifica os arquivos e diretórios que não devem ser versionados pelo Git.
- `pyproject.toml` e `poetry.lock`: arquivos utilizados pelo Poetry para gerenciamento de dependências.

<br>

## 🛠️ Tecnologias Utilizadas

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![HTTPX](https://img.shields.io/badge/HTTPX-333333?style=for-the-badge)](https://www.python-httpx.org/)
[![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![Poetry](https://img.shields.io/badge/Poetry-60A5FA?style=for-the-badge&logo=poetry&logoColor=white)](https://python-poetry.org/)
[![Podman](https://img.shields.io/badge/Podman-892CA0?style=for-the-badge&logo=podman&logoColor=white)](https://podman.io/)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)](https://github.com/features/actions)

<br>

## ▶️ Como Rodar o Projeto

1. **Clone o repositório:**

```bash
git clone https://github.com/RaykaDev/pokemon-api
```

2. **Navegue até a pasta do projeto:**

```bash
cd pokemon-api
```

3. **Instale as dependências com Poetry:**

```bash
poetry install
```

4. **Ative o ambiente virtual do Poetry:**

```bash
poetry shell
```

Caso prefira, também é possível executar os comandos utilizando `poetry run`, sem precisar ativar o ambiente virtual.

5. **Inicie a aplicação FastAPI:**

```bash
poetry run uvicorn app.main:app --reload
```

6. **Acesse a aplicação:**

```text
http://127.0.0.1:8000/
```

7. **Acesse a documentação interativa (Swagger UI):**

```text
http://127.0.0.1:8000/docs
```

<br>

## 📌 Endpoints

| Método | Rota             | Descrição                                     |
| ------ | ---------------- | --------------------------------------------- |
| `GET`  | `/`              | Rota inicial de boas-vindas                   |
| `GET`  | `/pokemons`      | Lista Pokémon com paginação                   |
| `GET`  | `/pokemons/{id}` | Consulta os detalhes de um Pokémon específico |

### Exemplos de requisição

**Listar Pokémon com paginação:**

```http
GET /pokemons?limit=20&offset=0
```

**Consultar um Pokémon pelo ID:**

```http
GET /pokemons/25
```

### Exemplo de resposta — Listagem paginada

```json
{
  "data": [
    {
      "name": "pikachu",
      "id": 25,
      "height": 4,
      "types": ["electric"],
      "sprites": {
        "front_default": "https://raw.githubusercontent.com/...",
        "back_default": "https://raw.githubusercontent.com/..."
      }
    }
  ],
  "pagination": {
    "total": 1350,
    "limit": 20,
    "offset": 0,
    "next": "/pokemons?limit=20&offset=20",
    "previous": null
  }
}
```

<br>

## 🧪 Testes

O projeto utiliza **Pytest** para executar testes automatizados, verificando o comportamento dos endpoints, a paginação, a validação dos parâmetros e o tratamento de erros.

**Executar os testes:**

```bash
poetry run pytest
```

**Executar os testes com relatório de cobertura:**

```bash
poetry run pytest --cov=app --cov-report=term-missing
```

O relatório permite visualizar a porcentagem de cobertura dos testes e identificar as linhas de código que ainda não foram executadas.

<br>

## 🐳 Docker / Podman

O projeto possui um `Dockerfile` para construir uma imagem da aplicação e executá-la em um contêiner.

Embora o arquivo utilize o padrão Dockerfile, a construção e execução foram realizadas com **Podman**.

**Construir a imagem:**

```bash
podman build -t pokemon-api .
```

**Executar o contêiner:**

```bash
podman run -d --name pokemon-api-container -p 8000:8000 pokemon-api
```

**Verificar os contêineres em execução:**

```bash
podman ps
```

**Visualizar os logs da aplicação:**

```bash
podman logs pokemon-api-container
```

<br>

## 🚀 Deploy

**URL de produção:** Em breve.

A aplicação será publicada em uma plataforma de hospedagem, permitindo o acesso público aos endpoints e à documentação interativa do FastAPI.

<br>

## 📌 Aprendizados

- Criação e organização de APIs REST com FastAPI
- Estruturação modular de projetos Python
- Separação de responsabilidades entre rotas e serviços
- Consumo de APIs externas utilizando HTTPX
- Realização de requisições HTTP e tratamento de respostas
- Manipulação e transformação de dados JSON
- Utilização de parâmetros de consulta (`query parameters`)
- Implementação de paginação com `limit` e `offset`
- Tratamento de exceções e erros HTTP com `HTTPException`
- Validação de parâmetros com `Query`
- Utilização de type hints nas funções
- Criação de testes automatizados com Pytest
- Simulação de falhas externas com `monkeypatch`
- Análise de cobertura de testes com Pytest-Cov
- Gerenciamento de dependências e ambiente virtual com Poetry
- Construção de imagens e execução de contêineres com Podman
- Documentação automática de APIs com Swagger UI
