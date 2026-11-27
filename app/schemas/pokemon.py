from pydantic import BaseModel, ConfigDict, Field


class PokemonCreate(BaseModel):
    nome: str = Field(
        description="Nome do Pokémon.",
        examples=["Pikachu"],
    )
    altura: int = Field(
        description="Altura do Pokémon.",
        examples=[4],
    )
    peso: int = Field(
        description="Peso do Pokémon.",
        examples=[60],
    )
    tipo: str = Field(
        description="Tipo do Pokémon.",
        examples=["Elétrico"],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "nome": "Pikachu",
                    "altura": 4,
                    "peso": 60,
                    "tipo": "Elétrico",
                }
            ]
        }
    )


class PokemonResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "id": 1,
                    "nome": "Pikachu",
                    "altura": 4,
                    "peso": 60,
                    "tipo": "Elétrico",
                }
            ]
        },
    )

    id: int = Field(description="Identificador único do Pokémon.")
    nome: str = Field(description="Nome do Pokémon.")
    altura: int = Field(description="Altura do Pokémon.")
    peso: int = Field(description="Peso do Pokémon.")
    tipo: str = Field(description="Tipo do Pokémon.")
