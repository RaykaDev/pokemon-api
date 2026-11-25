from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.crud import pokemon as pokemon_crud
from app.database import get_db
from app.schemas.pokemon import PokemonCreate, PokemonResponse
from app.services.pokeapi import pokemons_paginados, pokemon_por_id

router = APIRouter()


# CRUD - PostgreSQL


@router.post(
    "/pokemons",
    response_model=PokemonResponse,
    status_code=status.HTTP_201_CREATED,
)
def criar_pokemon(
    pokemon: PokemonCreate,
    db: Session = Depends(get_db),
):
    return pokemon_crud.create_pokemon(db, pokemon)


@router.get("/pokemons", response_model=list[PokemonResponse])
def listar_pokemons(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1),
    db: Session = Depends(get_db),
):
    return pokemon_crud.get_pokemons(db, skip, limit)


@router.get("/pokemons/{pokemon_id}", response_model=PokemonResponse)
def buscar_pokemon_banco(
    pokemon_id: int,
    db: Session = Depends(get_db),
):
    pokemon = pokemon_crud.get_pokemon(db, pokemon_id)

    if pokemon is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pokémon não encontrado.",
        )

    return pokemon


@router.put("/pokemons/{pokemon_id}", response_model=PokemonResponse)
def atualizar_pokemon(
    pokemon_id: int,
    pokemon_data: PokemonCreate,
    db: Session = Depends(get_db),
):
    pokemon = pokemon_crud.update_pokemon(db, pokemon_id, pokemon_data)

    if pokemon is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pokémon não encontrado.",
        )

    return pokemon


@router.delete("/pokemons/{pokemon_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_pokemon(
    pokemon_id: int,
    db: Session = Depends(get_db),
):
    excluido = pokemon_crud.delete_pokemon(db, pokemon_id)

    if not excluido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pokémon não encontrado.",
        )


# PokeAPI externa


@router.get("/pokeapi/pokemons")
def buscar_pokemons_externos(
    limit: int = Query(default=20, ge=1),
    offset: int = Query(default=0, ge=0),
):
    return pokemons_paginados(limit, offset)


@router.get("/pokeapi/pokemons/{id}")
def buscar_pokemon_externo(id: int):
    return pokemon_por_id(id)
