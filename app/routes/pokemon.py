from fastapi import APIRouter, Query
from app.services.pokeapi import pokemons_paginados, pokemon_por_id

router = APIRouter()


@router.get("/pokemons")
def buscar_pokemons(
    limit: int = Query(default=20, ge=1), offset: int = Query(default=0, ge=0)
):
    return pokemons_paginados(limit, offset)


@router.get("/pokemons/{id}")
def buscar_pokemon(id: int):
    return pokemon_por_id(id)
