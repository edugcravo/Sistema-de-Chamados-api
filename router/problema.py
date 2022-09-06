from datetime import datetime
from unittest import result
from fastapi import APIRouter, Response
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from schema.problema_schema import ProblemaSchema
from config.db import engine
from model.tipo_problema import problema
from typing import List

problemas = APIRouter()


@problemas.post("/problema/create")
def create_problema(problema_schema: ProblemaSchema):
  with engine.connect() as conn:
    try:
        tipo_problema = problema_schema.dict()
        print(tipo_problema)
        conn.execute(problema.insert().values(tipo_problema))
        
        return {"status": 200, "message": "Tipo de problema cadastrado com sucesso"}
    except:
        return {"status": 401, "message": "Erro ao cadastrar novo problema"}



@problemas.get("/problema/retorna-todos")
def retorna_todos():
  with engine.connect() as conn:
    try:
        result = conn.execute(problema.select()).fetchall() 
        
        return {"status": 200, "data": result}
    except:
        return {"status": 401, "message": "Erro ao cadastrar novo problema"}

