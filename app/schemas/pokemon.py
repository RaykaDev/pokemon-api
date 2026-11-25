from pydantic import BaseModel, ConfigDict


class PokemonCreate(BaseModel):
    nome: str
    altura: int
    peso: int
    tipo: str


class PokemonResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    altura: int
    peso: int
    tipo: str
