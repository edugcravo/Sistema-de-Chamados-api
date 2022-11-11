from datetime import datetime
from unittest import result
from fastapi import APIRouter, Response
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from config.db import engine
from model.log import logs
from typing import List

logs_router = APIRouter()


@logs_router.get("/logs/retorna-todos")
def retorna_todos():
  with engine.connect() as conn:
    try:
        result = conn.execute(logs.select()).fetchall() 
        
        return {"status": 200, "data": result}
    except:
        return {"status": 401, "message": "Erro ao cadastrar novo problema"}

