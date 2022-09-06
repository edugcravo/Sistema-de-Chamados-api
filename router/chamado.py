from datetime import datetime
from unittest import result
from fastapi import APIRouter, Response
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
from schema.chamado_schema import DataChamado, editaChamado
from config.db import engine
from model.chamado import chamados
from model.users import users
from model.tecnico import tecnicos
from typing import List

chamado = APIRouter()


@chamado.post("/chamado/create", status_code=HTTP_201_CREATED)
def create_user(DataChamado: DataChamado):
  with engine.connect() as conn:
    try:
        result = conn.execute(tecnicos.select().where(tecnicos.c.especialidade == DataChamado.tipo_problema)).first()
        print(result[0])
        quantidade_chamados = result[5] + 1
        
        id_tecnico = result[0]
        DataChamado.id_tecnico = id_tecnico
        DataChamado.data_hora_criacao = datetime.utcnow()
        DataChamado.status = 'Criado'
        novo_chamado = DataChamado.dict()
        conn.execute(chamados.insert().values(novo_chamado))
        
        conn.execute(tecnicos.update().values(qtd_chamado=quantidade_chamados).where(tecnicos.c.id == result[0]))
        return {"status": 200, "message": "Chamado Cadastrado"}, 
    except:
        return {"status": 401, "message": "Erro ao cadastrar Chamado"}


@chamado.get("/chamado/retorna-id-tecnico")
def get_user(id_user: str):
  with engine.connect() as conn:
    user = []
    resultado = conn.execute(chamados.select().where(chamados.c.id_tecnico == id_user)).fetchall() 
    for i in resultado:

      todos_usuarios = conn.execute(users.select().where(users.c.id == i[9])).fetchall()
      usuarios = todos_usuarios[0][1]
      user.append(usuarios)
  
    return {'chamado':resultado, 'usuarios': user}



@chamado.get("/chamado/retorna-id")
def get_user(id_chamado: int):
  with engine.connect() as conn:
    result = conn.execute(chamados.select().where(chamados.c.id == id_chamado)).fetchall() 
    print(result)
    id_usuario = result[0][9]
    user = conn.execute(users.select().where(users.c.id == id_usuario)).first()


    return {'chamado':result[0] ,'usuario': user}



@chamado.get("/chamado/retorna-nome-usuario")
def get_user(id_usuario: int):
  with engine.connect() as conn:
    result = conn.execute(chamados.select().where(chamados.c.id_usuario == id_usuario)).fetchall()
    ids_tecnicos = []
    for i in result:
      print(i[8])
      todos_tecnicos = conn.execute(tecnicos.select().where(tecnicos.c.id == i[8])).fetchall()
      ids_tecnicos.append(todos_tecnicos[0])
    
    
    return {'chamado':result, 'tecnicos': ids_tecnicos}


@chamado.get("/chamado/retorna-chamados")
def get_user():
  with engine.connect() as conn:
    result = conn.execute(chamados.select()).fetchall() 

    return {'chamado':result}


@chamado.put("/chamado/update_chamado", response_model=editaChamado)
def update_user(data_update: editaChamado, id_chamado: int):
  with engine.connect() as conn:
    try:
      conn.execute(chamados.update().values(resolucao_problema=data_update.resolucao_problema, tipo_problema=data_update.tipo_problema, status=data_update.status).where(chamados.c.id == id_chamado))

      result = conn.execute(chamados.select().where(chamados.c.id == id_chamado)).first()
      return result
    except:
      return {"status": 401, "message": "Erro ao cadastrar Chamado"}


# select chamados format(data_hora_criacao,'dd/MM/yyyy HH:mm:ss') as data_hora_criacao from  'chamados'
# where CAST(data_hora_criacao as date) between cast( dateadd (day,-7,getdate()) as date) and  cast (getdate() as date)
