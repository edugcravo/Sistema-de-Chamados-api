from ast import And
from unittest import result
from fastapi import APIRouter, Response, Header
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
from config.db import engine
from model.acompanhamento import acompanhamentos

from typing import List, Optional



acompanhamentos_router = APIRouter(
    prefix="/acompanhamento",
    tags=["Acompanhamento"],
)

@acompanhamentos_router.get("/")
def root():
  return {"message": "Hi, I am FastAPI with a router"}


@acompanhamentos_router.get("/retorna-id-chamado")
def get_user(id: int):
  with engine.connect() as conn:
    print(id)
    resultado = conn.execute(acompanhamentos.select().where(acompanhamentos.c.id_chamado == id)).fetchall() 
  
    return {'respostas':resultado}