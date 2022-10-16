from datetime import datetime
from unittest import result
from fastapi import APIRouter, Response
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
from schema.chamado_schema import DataChamado, editaChamado
from config.db import engine
from model.chamado import chamados
from model.users import users
from model.tecnico import tecnicos
from model.log import logs
from model.acompanhamento import acompanhamentos
from typing import List


chamado_router = APIRouter(
    prefix="/chamado",
    tags=["Chamado"],
)



@chamado_router.post("/create", status_code=HTTP_201_CREATED)
def create_user(DataChamado: DataChamado):
  with engine.connect() as conn:
    try:
        result = conn.execute(tecnicos.select().where(tecnicos.c.especialidade == DataChamado.tipo_problema)).first()
        quantidade_chamados = result[5] + 1
        
        id_tecnico = result[0]
        DataChamado.id_tecnico = id_tecnico
        DataChamado.data_hora_criacao = datetime.utcnow()
        DataChamado.status = 'Criado'
        novo_chamado = DataChamado.dict()
        conn.execute(chamados.insert().values(novo_chamado))

        # Pegando chamado para obter id dele
        chamado = conn.execute(chamados.select().where(chamados.c.id_equipamento == novo_chamado['id_equipamento'] and chamados.c.local == novo_chamado['local'] and chamados.c.ramal == novo_chamado['ramal'] and chamados.c.tipo_problema == novo_chamado['tipo_problema'] and chamados.c.desc_problema == novo_chamado['desc_problema'] and chamados.c.status == novo_chamado['status'] and chamados.c.id_tecnico == novo_chamado['id_tecnico'] and chamados.c.id_usuario == novo_chamado['id_usuario'] and chamados.c.data_hora_criacao == novo_chamado['data_hora_criacao'])).first()

        acompanhamento_chamado = {
          'id_chamado': chamado[0],
          'data':datetime.utcnow(),
          'resposta': 'chamado criado',
          'tecnico': False
        }

        # Criando tabela de acompanhamento
        conn.execute(acompanhamentos.insert().values(acompanhamento_chamado))


        conn.execute(logs.insert().values(tipo='chamado',date=datetime.utcnow(), acao='create', object_id=1))

        conn.execute(tecnicos.update().values(qtd_chamado=quantidade_chamados).where(tecnicos.c.id == result[0]))
        return {"status": 200, "message": "Chamado Cadastrado"}, 
    except:
        return {"status": 401, "message": "Erro ao cadastrar Chamado"}



@chamado_router.get("/retorna-id-tecnico")
def get_user(id_tecnico: str):
  with engine.connect() as conn:
    user = []
    resultado = conn.execute(chamados.select().where(chamados.c.id_tecnico == id_tecnico)).fetchall() 
    for i in resultado:

      todos_usuarios = conn.execute(users.select().where(users.c.id == i[9])).fetchall()
      usuarios = todos_usuarios[0][1]
      user.append(usuarios)
  
    return {'chamado':resultado, 'usuarios': user}



@chamado_router.get("/retorna-id")
def get_user(id_chamado: int):
  with engine.connect() as conn:
    result = conn.execute(chamados.select().where(chamados.c.id == id_chamado)).fetchall() 
    id_tecnico = result[0][8]
    id_usuario = result[0][9]
    user = conn.execute(users.select().where(users.c.id == id_usuario)).first()
    tecnico = conn.execute(tecnicos.select().where(tecnicos.c.id == id_tecnico)).first()



    return {'chamado':result[0] ,'usuario': user, 'tecnico': tecnico}



@chamado_router.get("/retorna-id-usuario")
def get_user(id_usuario: int):
  with engine.connect() as conn:
    result = conn.execute(chamados.select().where(chamados.c.id_usuario == id_usuario)).fetchall()
    ids_tecnicos = []
    for i in result:
      todos_tecnicos = conn.execute(tecnicos.select().where(tecnicos.c.id == i[8])).fetchall()
      ids_tecnicos.append(todos_tecnicos[0])
    
    
    return {'chamado':result, 'tecnicos': ids_tecnicos}


@chamado_router.get("/retorna-chamados")
def get_user():
  with engine.connect() as conn:
    result = conn.execute(chamados.select()).fetchall() 

    return {'chamado':result}


@chamado_router.put("/update_chamado", response_model=editaChamado)
def update_user(data_update: editaChamado, id_chamado: int, tecnico: int):
  with engine.connect() as conn:
    try:
      print(tecnico)
      conn.execute(chamados.update().values(tipo_problema=data_update.tipo_problema, status=data_update.status).where(chamados.c.id == id_chamado))

      acompanhamento_chamado = {
          'id_chamado': id_chamado,
          'data':datetime.utcnow(),
          'resposta': data_update.resolucao_problema,
          'tecnico': tecnico
        }

        # Criando tabela de acompanhamento
      conn.execute(acompanhamentos.insert().values(acompanhamento_chamado))

      result = conn.execute(chamados.select().where(chamados.c.id == id_chamado)).first()
      return result
    except:
      return {"status": 401, "message": "Erro ao cadastrar Chamado"}


# select chamados format(data_hora_criacao,'dd/MM/yyyy HH:mm:ss') as data_hora_criacao from  'chamados'
# where CAST(data_hora_criacao as date) between cast( dateadd (day,-7,getdate()) as date) and  cast (getdate() as date)
