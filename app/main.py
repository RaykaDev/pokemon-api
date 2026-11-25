from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import create_tables
from app.routes.pokemon import router as pokemons_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(pokemons_router)


@app.get("/")
async def root():
    return {"message": "API de Pokémon"}
