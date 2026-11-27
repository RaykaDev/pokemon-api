from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
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
    summary="Cadastrar um Pokémon",
    description="Cadastra um novo Pokémon no banco de dados PostgreSQL.",
    response_description="Pokémon cadastrado com sucesso.",
    responses={
        201: {
            "description": "Pokémon cadastrado com sucesso.",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "nome": "Pikachu",
                        "altura": 4,
                        "peso": 60,
                        "tipo": "Elétrico",
                    }
                }
            },
        }
    },
)
def criar_pokemon(
    pokemon: PokemonCreate = Body(
        openapi_examples={
            "pikachu": {
                "summary": "Cadastro de Pikachu",
                "description": "Exemplo de cadastro de um Pokémon.",
                "value": {
                    "nome": "Pikachu",
                    "altura": 4,
                    "peso": 60,
                    "tipo": "Elétrico",
                },
            }
        }
    ),
    db: Session = Depends(get_db),
):
    return pokemon_crud.create_pokemon(db, pokemon)


@router.get(
    "/pokemons",
    response_model=list[PokemonResponse],
    summary="Listar Pokémon cadastrados",
    description="Retorna uma lista de Pokémon armazenados no banco de dados, com suporte a paginação.",
    response_description="Lista de Pokémon cadastrados.",
    responses={
        200: {
            "description": "Lista retornada com sucesso.",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "nome": "Pikachu",
                            "altura": 4,
                            "peso": 60,
                            "tipo": "Elétrico",
                        }
                    ]
                }
            },
        }
    },
)
def listar_pokemons(
    skip: int = Query(
        default=0, ge=0, description="Quantidade de registros a ignorar."
    ),
    limit: int = Query(
        default=100, ge=1, description="Quantidade máxima de registros retornados."
    ),
    db: Session = Depends(get_db),
):
    return pokemon_crud.get_pokemons(db, skip, limit)


@router.get(
    "/pokemons/{pokemon_id}",
    response_model=PokemonResponse,
    summary="Buscar Pokémon por ID",
    description="Consulta um Pokémon cadastrado no banco de dados utilizando seu identificador.",
    response_description="Dados do Pokémon encontrado.",
    responses={
        200: {
            "description": "Pokémon encontrado.",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "nome": "Pikachu",
                        "altura": 4,
                        "peso": 60,
                        "tipo": "Elétrico",
                    }
                }
            },
        },
        404: {
            "description": "Pokémon não encontrado.",
            "content": {
                "application/json": {"example": {"detail": "Pokémon não encontrado."}}
            },
        },
    },
)
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


@router.put(
    "/pokemons/{pokemon_id}",
    response_model=PokemonResponse,
    summary="Atualizar um Pokémon",
    description="Atualiza os dados de um Pokémon existente no banco de dados.",
    response_description="Pokémon atualizado com sucesso.",
    responses={
        200: {
            "description": "Pokémon atualizado.",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "nome": "Pikachu",
                        "altura": 4,
                        "peso": 60,
                        "tipo": "Elétrico",
                    }
                }
            },
        },
        404: {
            "description": "Pokémon não encontrado.",
            "content": {
                "application/json": {"example": {"detail": "Pokémon não encontrado."}}
            },
        },
    },
)
def atualizar_pokemon(
    pokemon_id: int,
    pokemon_data: PokemonCreate = Body(
        openapi_examples={
            "pikachu_atualizado": {
                "summary": "Atualização de Pikachu",
                "description": "Exemplo de atualização dos dados de um Pokémon.",
                "value": {
                    "nome": "Pikachu",
                    "altura": 4,
                    "peso": 60,
                    "tipo": "Elétrico",
                },
            }
        }
    ),
    db: Session = Depends(get_db),
):
    pokemon = pokemon_crud.update_pokemon(db, pokemon_id, pokemon_data)

    if pokemon is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pokémon não encontrado.",
        )

    return pokemon


@router.delete(
    "/pokemons/{pokemon_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir um Pokémon",
    description="Exclui permanentemente um Pokémon do banco de dados utilizando seu identificador.",
    response_description="Registro excluído. Nenhum conteúdo é retornado.",
    responses={
        204: {"description": "Pokémon excluído com sucesso. Resposta sem conteúdo."},
        404: {
            "description": "Pokémon não encontrado.",
            "content": {
                "application/json": {"example": {"detail": "Pokémon não encontrado."}}
            },
        },
    },
)
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


@router.get(
    "/pokeapi/pokemons",
    summary="Listar Pokémon da PokeAPI",
    description="Consulta Pokémon na PokeAPI externa e retorna seus dados com paginação.",
    response_description="Lista de Pokémon com informações de paginação.",
    responses={
        200: {
            "description": "Pokémon retornados com sucesso.",
            "content": {
                "application/json": {
                    "example": {
                        "data": [
                            {
                                "name": "pikachu",
                                "id": 25,
                                "height": 4,
                                "types": ["electric"],
                                "sprites": {
                                    "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png",
                                    "back_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/25.png",
                                },
                            }
                        ],
                        "pagination": {
                            "total": 1351,
                            "limit": 20,
                            "offset": 0,
                            "next": "/pokeapi/pokemons?limit=20&offset=20",
                            "previous": None,
                        },
                    }
                }
            },
        },
        503: {"description": "Serviço externo indisponível."},
    },
)
def buscar_pokemons_externos(
    limit: int = Query(
        default=20, ge=1, description="Quantidade de Pokémon por página."
    ),
    offset: int = Query(
        default=0, ge=0, description="Quantidade de registros a ignorar."
    ),
):
    return pokemons_paginados(limit, offset)


@router.get(
    "/pokeapi/pokemons/{id}",
    summary="Buscar Pokémon na PokeAPI",
    description="Consulta os detalhes de um Pokémon na PokeAPI externa utilizando seu ID.",
    response_description="Dados detalhados do Pokémon consultado.",
    responses={
        200: {
            "description": "Pokémon encontrado.",
            "content": {
                "application/json": {
                    "example": {
                        "id": 25,
                        "name": "pikachu",
                        "height": 4,
                        "types": ["electric"],
                        "sprites": {
                            "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png",
                            "back_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/25.png",
                        },
                    }
                }
            },
        },
        404: {"description": "Pokémon não encontrado."},
        503: {"description": "Serviço externo indisponível."},
    },
)
def buscar_pokemon_externo(id: int):
    return pokemon_por_id(id)
