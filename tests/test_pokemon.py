from fastapi.testclient import TestClient
from app.main import app
import httpx

client = TestClient(app)


def test_buscar_pokemon():
    resposta = client.get("/pokemons")

    assert resposta.status_code == 200
    assert isinstance(resposta.json()["data"], list)
    assert isinstance(resposta.json()["pagination"], dict)


def test_paginacao():
    resposta = client.get("/pokemons?limit=2&offset=2")

    assert resposta.status_code == 200
    assert resposta.json()["pagination"]["limit"] == 2
    assert resposta.json()["pagination"]["offset"] == 2
    assert len(resposta.json()["data"]) == 2
    assert resposta.json()["pagination"]["next"] == "/pokemons?limit=2&offset=4"
    assert resposta.json()["pagination"]["previous"] == "/pokemons?limit=2&offset=0"


def test_buscar_pokemon_por_id():
    resposta = client.get("/pokemons/25")

    assert resposta.status_code == 200
    assert isinstance(resposta.json(), dict)
    assert resposta.json()["id"] == 25
    assert resposta.json()["name"] == "pikachu"
    assert isinstance(resposta.json()["types"], list)
    assert isinstance(resposta.json()["sprites"], dict)


def test_pokemon_nao_encontrado():
    resposta = client.get("/pokemons/99999")

    assert resposta.status_code == 404
    assert resposta.json()["detail"] == "Pokémon não encontrado"


def test_limit_invalido():
    resposta = client.get("/pokemons?limit=0")

    assert resposta.status_code == 422


def test_offset_invalido():
    resposta = client.get("/pokemons?offset=-1")

    assert resposta.status_code == 422


def test_rota_inicial():
    resposta = client.get("/")

    assert resposta.status_code == 200
    assert resposta.json()["message"] == "API de Pokémon"


def test_erro_conexao_pokeapi(monkeypatch):
    def lancar_error(*args, **kwargs):
        raise httpx.RequestError(
            "Falha de conexão", request=httpx.Request("GET", "https://pokeapi.co")
        )

    monkeypatch.setattr("app.services.pokeapi.httpx.get", lancar_error)
    resposta = client.get("/pokemons")
    assert resposta.status_code == 503
