from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.pokemon import Pokemon
from app.schemas.pokemon import PokemonCreate


def create_pokemon(db: Session, pokemon: PokemonCreate) -> Pokemon:
    db_pokemon = Pokemon(**pokemon.model_dump())

    db.add(db_pokemon)
    db.commit()
    db.refresh(db_pokemon)

    return db_pokemon


def get_pokemon(db: Session, pokemon_id: int) -> Pokemon | None:
    return db.get(Pokemon, pokemon_id)


def get_pokemons(db: Session, skip: int = 0, limit: int = 100) -> list[Pokemon]:
    statement = select(Pokemon).offset(skip).limit(limit)
    return list(db.scalars(statement).all())


def update_pokemon(
    db: Session,
    pokemon_id: int,
    pokemon_data: PokemonCreate,
) -> Pokemon | None:
    db_pokemon = db.get(Pokemon, pokemon_id)

    if db_pokemon is None:
        return None

    for campo, valor in pokemon_data.model_dump().items():
        setattr(db_pokemon, campo, valor)

    db.commit()
    db.refresh(db_pokemon)

    return db_pokemon


def delete_pokemon(db: Session, pokemon_id: int) -> bool:
    db_pokemon = db.get(Pokemon, pokemon_id)

    if db_pokemon is None:
        return False

    db.delete(db_pokemon)
    db.commit()

    return True
