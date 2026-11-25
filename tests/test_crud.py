import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import get_db
from app.models.pokemon import Base

test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False,
)


@pytest.fixture
def client():
    Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    test_client = TestClient(app)
    yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)


def test_criar_pokemon(client):
    resposta = client.post(
        "/pokemons",
        json={
            "nome": "Pikachu",
            "altura": 4,
            "peso": 60,
            "tipo": "Elétrico",
        },
    )

    assert resposta.status_code == 201
    assert resposta.json()["nome"] == "Pikachu"
    assert resposta.json()["id"] is not None


def test_listar_pokemons(client):
    client.post(
        "/pokemons",
        json={
            "nome": "Pikachu",
            "altura": 4,
            "peso": 60,
            "tipo": "Elétrico",
        },
    )

    resposta = client.get("/pokemons")

    assert resposta.status_code == 200
    assert len(resposta.json()) == 1
    assert resposta.json()[0]["nome"] == "Pikachu"


def test_buscar_pokemon_por_id_banco(client):
    criado = client.post(
        "/pokemons",
        json={
            "nome": "Charmander",
            "altura": 6,
            "peso": 85,
            "tipo": "Fogo",
        },
    )

    pokemon_id = criado.json()["id"]
    resposta = client.get(f"/pokemons/{pokemon_id}")

    assert resposta.status_code == 200
    assert resposta.json()["nome"] == "Charmander"


def test_atualizar_pokemon(client):
    criado = client.post(
        "/pokemons",
        json={
            "nome": "Bulbasaur",
            "altura": 7,
            "peso": 69,
            "tipo": "Planta",
        },
    )

    pokemon_id = criado.json()["id"]

    resposta = client.put(
        f"/pokemons/{pokemon_id}",
        json={
            "nome": "Ivysaur",
            "altura": 10,
            "peso": 130,
            "tipo": "Planta",
        },
    )

    assert resposta.status_code == 200
    assert resposta.json()["nome"] == "Ivysaur"


def test_excluir_pokemon(client):
    criado = client.post(
        "/pokemons",
        json={
            "nome": "Squirtle",
            "altura": 5,
            "peso": 90,
            "tipo": "Água",
        },
    )

    pokemon_id = criado.json()["id"]
    resposta = client.delete(f"/pokemons/{pokemon_id}")

    assert resposta.status_code == 204

    busca = client.get(f"/pokemons/{pokemon_id}")
    assert busca.status_code == 404


def test_buscar_pokemon_inexistente_banco(client):
    resposta = client.get("/pokemons/99999")

    assert resposta.status_code == 404


def test_atualizar_pokemon_inexistente(client):
    resposta = client.put(
        "/pokemons/99999",
        json={
            "nome": "Mewtwo",
            "altura": 20,
            "peso": 1220,
            "tipo": "Psíquico",
        },
    )

    assert resposta.status_code == 404


def test_excluir_pokemon_inexistente(client):
    resposta = client.delete("/pokemons/99999")

    assert resposta.status_code == 404
