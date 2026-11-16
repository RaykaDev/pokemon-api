from fastapi import FastAPI
from app.routes.pokemon import router as pokemons_router

# as cria um apelido para o router do arquivo routes


app = FastAPI()
app.include_router(pokemons_router)


@app.get("/")
async def root():
    return {"message": "API de Pokémon"}
