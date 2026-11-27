import httpx
from fastapi import HTTPException


def pokemons_paginados(limit: int = 20, offset: int = 0) -> dict:
    # Lista de pokémons
    try:
        requisicao = httpx.get(
            f"https://pokeapi.co/api/v2/pokemon?limit={limit}&offset={offset}",
            timeout=10.0,
        )
        requisicao.raise_for_status()

        dados = requisicao.json()
        detalhes_pokemon = []

        for pokemon in dados["results"]:
            detalhes = obter_detalhes_pokemon(pokemon["url"])
            tipos_pokemon = []

            for tipo in detalhes["types"]:
                tipos_pokemon.append(tipo["type"]["name"])

            pokemon_formatado = {
                "name": detalhes["name"],
                "id": detalhes["id"],
                "height": detalhes["height"],
                "types": tipos_pokemon,
                "sprites": {
                    "front_default": detalhes["sprites"]["front_default"],
                    "back_default": detalhes["sprites"]["back_default"],
                },
            }

            detalhes_pokemon.append(pokemon_formatado)

    except httpx.HTTPStatusError as erro:
        raise HTTPException(
            status_code=503,
            detail="PokeAPI está indisponível.",
        ) from erro

    except httpx.RequestError as erro:
        raise HTTPException(
            status_code=503,
            detail="Não foi possível estabelecer conexão com a PokeAPI.",
        ) from erro

    proximo_offset = offset + limit
    anterior_offset = max(0, offset - limit)

    proximo = (
        f"/pokeapi/pokemons?limit={limit}&offset={proximo_offset}"
        if dados["next"] is not None
        else None
    )

    anterior = (
        f"/pokeapi/pokemons?limit={limit}&offset={anterior_offset}"
        if offset > 0
        else None
    )

    resposta = {
        "data": detalhes_pokemon,
        "pagination": {
            "total": dados["count"],
            "limit": limit,
            "offset": offset,
            "next": proximo,
            "previous": anterior,
        },
    }

    return resposta


def obter_detalhes_pokemon(url: str) -> dict:
    try:
        requisicao = httpx.get(url, timeout=10.0)
        requisicao.raise_for_status()

    except httpx.HTTPStatusError:
        raise

    except httpx.RequestError as erro:
        raise HTTPException(
            status_code=503,
            detail="PokeAPI está indisponível.",
        ) from erro

    dados = requisicao.json()
    return dados


def pokemon_por_id(id: int) -> dict:
    url = f"https://pokeapi.co/api/v2/pokemon/{id}"

    try:
        detalhes = obter_detalhes_pokemon(url)

    except httpx.HTTPStatusError as erro:
        if erro.response.status_code == 404:
            raise HTTPException(
                status_code=404,
                detail="Pokémon não encontrado",
            ) from erro

        raise HTTPException(
            status_code=503,
            detail="PokeAPI está indisponível.",
        ) from erro

    tipos_pokemon = []

    for tipo in detalhes["types"]:
        tipos_pokemon.append(tipo["type"]["name"])

    pokemons = {
        "id": detalhes["id"],
        "name": detalhes["name"],
        "height": detalhes["height"],
        "types": tipos_pokemon,
        "sprites": {
            "front_default": detalhes["sprites"]["front_default"],
            "back_default": detalhes["sprites"]["back_default"],
        },
    }

    return pokemons
