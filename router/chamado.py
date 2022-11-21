import base64
from datetime import datetime
from io import BytesIO
from typing import List
from unittest import result

from fastapi import APIRouter, Response
from starlette.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                              HTTP_401_UNAUTHORIZED)

from config.db import engine
from model.acompanhamento import acompanhamentos
from model.chamado import chamados
from model.log import logs
from model.tecnico import tecnicos
from model.tipo_problema import problemas
from model.users import users
from schema.chamado_schema import DataChamado, cancelaChamado, editaChamado, filtroChamado

chamado_router = APIRouter(
    prefix="/chamado",
    tags=["Chamado"],
)



@chamado_router.get("/")
def root():
  return {"message": "Testando end point"}


@chamado_router.post("/create", status_code=HTTP_201_CREATED)
def create_user(DataChamado: DataChamado):
  with engine.connect() as conn:
    try:
    
        
        # Pegando o tipo de problema, para buscar o tecnico
        tipo_problema = conn.execute(problemas.select().where(problemas.c.id == DataChamado.tipo_problema)).first()
        tipo_problema = tipo_problema['tipo_problema']

        # Pegando o tecnico com a especialidade igual a do tipo do problema
        result = conn.execute(tecnicos.select().where(tecnicos.c.especialidade == tipo_problema)).first()
        print(result)
        # Aumentando a quantidade de chamados do tecnico
        quantidade_chamados = result['qtd_chamado'] + 1

        #colocando id do tecnico no result
        id_tecnico = result[0]

        DataChamado.id_tecnico = id_tecnico
        DataChamado.data_hora_criacao = datetime.utcnow()
        DataChamado.status = 'em andamento'
        
        novo_chamado = DataChamado.dict()
        #Inserindo o chamado no banco
        conn.execute(chamados.insert().values(novo_chamado))

        # Pegando chamado para obter id dele
        chamado = conn.execute(chamados.select().where(chamados.c.id_equipamento == novo_chamado['id_equipamento'] and chamados.c.local == novo_chamado['local'] and chamados.c.ramal == novo_chamado['ramal'] and chamados.c.tipo_problema == novo_chamado['tipo_problema'] and chamados.c.desc_problema == novo_chamado['desc_problema'] and chamados.c.status == novo_chamado['status'] and chamados.c.id_tecnico == novo_chamado['id_tecnico'] and chamados.c.id_usuario == novo_chamado['id_usuario'] and chamados.c.data_hora_criacao == novo_chamado['data_hora_criacao'])).first()

        acompanhamento_chamado = {
          'id_chamado': chamado[0],
          'data':datetime.utcnow(),
          'resposta': 'chamado criado',
          'tecnico': True
        }


        # Criando tabela de acompanhamento
        conn.execute(acompanhamentos.insert().values(acompanhamento_chamado))

        # Criando log do chamado
        conn.execute(logs.insert().values(tipo='chamado',date=datetime.utcnow(), acao='create', object_id=chamado[0]))

        # atualizando quantidade de chamados do tecnico
        conn.execute(tecnicos.update().values(qtd_chamado=quantidade_chamados).where(tecnicos.c.id == result[0]))
        return {"status": 200, "message": "Chamado Cadastrado"}, 
    except:
        return {"status": 401, "message": "Erro ao cadastrar Chamado"}



#Retorna todos os chamados por id tecnico
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

    #pegando o tipo do problema
    tipo_problema = conn.execute(problemas.select().where(problemas.c.id == result[0]['tipo_problema'])).fetchall() 

    chamado = list([result[0]])


    # result[0]['tipo_problema'] = tipo_problema[0]['tipo_problema']

    # result[0][4] = tipo_problema
    id_tecnico = result[0][8]
    id_usuario = result[0][9]
    user = conn.execute(users.select().where(users.c.id == id_usuario)).first()
    tecnico = conn.execute(tecnicos.select().where(tecnicos.c.id == id_tecnico)).first()


    return {'chamado':result[0] ,'usuario': user, 'tecnico': tecnico, 'problema': tipo_problema[0]['tipo_problema']}


#Retorna todos os chamados por id do usuario
@chamado_router.get("/retorna-id-usuario")
def get_user(id_usuario: int):
  with engine.connect() as conn:
    result = conn.execute(chamados.select().where(chamados.c.id_usuario == id_usuario)).fetchall()
    ids_tecnicos = []
    for i in result:
      print(i)
      todos_tecnicos = conn.execute(tecnicos.select().where(tecnicos.c.id == i[8])).fetchall()
      ids_tecnicos.append(todos_tecnicos[0])
    
    
    return {'chamado':result, 'tecnicos': ids_tecnicos}



#Retorna todos os chamados por id do usuario
@chamado_router.post("/retorna-por-filtro")
def get_filtro(dataChamado: filtroChamado):
  with engine.connect() as conn:

    result = (conn.execute(chamados.select().where(chamados.c.tipo_problema.in_(dataChamado.problema) & chamados.c.local.in_(dataChamado.setor)))).fetchall()

    return {'chamado':result}

    


@chamado_router.get("/retorna-chamados")
def get_user():
  with engine.connect() as conn:
    result = conn.execute(chamados.select()).fetchall() 

    todos_tecnicos = conn.execute(tecnicos.select()).fetchall()

    return {'chamado':result, 'tecnicos': todos_tecnicos}


@chamado_router.put("/update_chamado", response_model=editaChamado)
def update_user(data_update: editaChamado, id_chamado: int, tecnico: int):
  with engine.connect() as conn:
    try:

      
      result = conn.execute(tecnicos.select().where(tecnicos.c.especialidade == data_update.tipo_problema)).first()
      print(data_update.tipo_problema)
      problem = conn.execute(problemas.select().where(problemas.c.tipo_problema == data_update.tipo_problema)).first()

      print('-----------------------')
      

      conn.execute(chamados.update().values(tipo_problema=problem['id'], status=data_update.status, id_tecnico=result['id']).where(chamados.c.id == id_chamado))

      
      
      print(data_update)

      #Inserindo resposta na tabela 
      acompanhamento_chamado = {
          'id_chamado': id_chamado,
          'data':datetime.utcnow(),
          'resposta': data_update.resolucao_problema,
          'tecnico': tecnico
        }

      print(tecnico)
      

        # inserindo tabela de acompanhamento
      conn.execute(acompanhamentos.insert().values(acompanhamento_chamado))

      if tecnico == 1:
        resposta = 'resposta do usuario'
      else:
        resposta = 'resposta do tecnico'

      conn.execute(logs.insert().values(tipo='chamado',date=datetime.utcnow(), acao=resposta, object_id=id_chamado))

      result = conn.execute(chamados.select().where(chamados.c.id == id_chamado)).first()
      return result
    except:
      return {"status": 401, "message": "Erro ao cadastrar Chamado"}


  
@chamado_router.put("/cancela_ou_reabre_chamado", response_model=editaChamado)
def update_user(data_update: cancelaChamado, id_chamado: int, tecnico: int):
  with engine.connect() as conn:
    try:
      print(tecnico)
      conn.execute(chamados.update().values(status=data_update.status).where(chamados.c.id == id_chamado))

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
      return {"status": 401, "message": "Erro ao cancelar Chamado"}


# def convert_image_to_b64(image):
#     buffered = BytesIO()
#     image.save(buffered, format="JPEG")
#     img_str = base64.b64encode(buffered.getvalue())
#     return img_str.decode('utf-8')
# select chamados format(data_hora_criacao,'dd/MM/yyyy HH:mm:ss') as data_hora_criacao from  'chamados'
# where CAST(data_hora_criacao as date) between cast( dateadd (day,-7,getdate()) as date) and  cast (getdate() as date)
