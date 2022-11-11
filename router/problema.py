from datetime import datetime
from unittest import result
from fastapi import APIRouter, Response
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from schema.problema_schema import ProblemaSchema
from config.db import engine
from model.tipo_problema import problemas
from typing import List

problemas_router = APIRouter()


@problemas_router.post("/problema/create")
def create_problema(problema_schema: ProblemaSchema):
  with engine.connect() as conn:
    try:
        tipo_problema = problema_schema.dict()
        conn.execute(problemas.insert().values(tipo_problema))
        
        return {"status": 200, "message": "Tipo de problema cadastrado com sucesso"}
    except:
        return {"status": 401, "message": "Erro ao cadastrar novo problema"}



@problemas_router.get("/problema/retorna-todos")
def retorna_todos():
  with engine.connect() as conn:
    try:
        result = conn.execute(problemas.select()).fetchall() 
        
        return {"status": 200, "data": result}
    except:
        return {"status": 401, "message": "Erro ao cadastrar novo problema"}

