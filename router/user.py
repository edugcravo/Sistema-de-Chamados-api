from ast import And
from unittest import result
from fastapi import APIRouter, Response
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
from schema.tecnico_schema import TecnicoSchema, DataTecnicoImg
from schema.user_schema import UserSchema, DataUser, DataUserImg
from config.db import engine
from model.users import users
from model.tecnico import tecnicos
from werkzeug.security import generate_password_hash, check_password_hash
from typing import List, Optional

user_router = APIRouter()



@user_router.get("/retorna_users", response_model=List[UserSchema])
def get_users():
  with engine.connect() as conn:
    result = conn.execute(users.select()).fetchall() 
    return result


@user_router.get("/retorna_users_id/", response_model=UserSchema)
def get_user(user_id: str):
  with engine.connect() as conn:
    result = conn.execute(users.select().where(users.c.id == user_id)).first()

    return result


#Tela de informacoes
@user_router.get("/retorna_users_nome")
def get_user(nome_user: str):
  with engine.connect() as conn:
    try:
      result = conn.execute(users.select().where(users.c.username == nome_user)).first()
      if result == None:
        result = conn.execute(tecnicos.select().where(tecnicos.c.username == nome_user)).first()
        if result == None:
          return {'message': 'Usuário não encontrado'}
        return {'usuario': result}
      else:
        nome_usuario = result[2]
        setor_usuario = result[5]
        #Selecionando todos usuarios do setor
        users_setores = conn.execute(users.select().where(users.c.setor == setor_usuario, users.c.username != nome_usuario)).fetchall() 
        return {'usuario': result, 'usuarios_setores': users_setores}
    except:
      return {'message': 'Erro ao buscar usuario'}
    
      
      
    


@user_router.post("/cria_user", status_code=HTTP_201_CREATED)
def create_user(data_user: UserSchema):
  with engine.connect() as conn:
    try:
      new_user = data_user.dict()
      new_user["user_passw"] = generate_password_hash(data_user.user_passw, "pbkdf2:sha256:30", 30)

      conn.execute(users.insert().values(new_user))

      return {'data':Response(status_code=HTTP_201_CREATED), 'message': 'Usuario criado com sucesso'}
    except:
      return {'message': 'Erro ao criar usuario'}


@user_router.post("/cria_tecnico", status_code=HTTP_201_CREATED)
def create_user(data_user: TecnicoSchema):
  with engine.connect() as conn:
    try:
      new_user = data_user.dict()
      new_user["user_passw"] = generate_password_hash(data_user.user_passw, "pbkdf2:sha256:30", 30)

      conn.execute(tecnicos.insert().values(new_user))

      return {'data':Response(status_code=HTTP_201_CREATED), 'message': 'Tecnico criado com sucesso'}
    except:
      return {'message': 'Erro ao criar Tecnico'}



@user_router.post("/user/login", status_code=200)
def user_login(data_user: DataUser):
  with engine.connect() as conn:
    result = conn.execute(users.select().where(users.c.username == data_user.username)).first()
    resultTecnico = conn.execute(tecnicos.select().where(tecnicos.c.username == data_user.username)).first()


    if result != None:
      print(data_user.user_passw)
      print(result)
      check_passw = check_password_hash(result[7], data_user.user_passw)
      print(check_passw)

      if check_passw:
        return {
          "status": 200,
          "message": "Access success",
          "id": result[0]
        }
      else:
        return{
          "status": 401,
          "message": "Access denied"
        }

    elif resultTecnico != None:
      check_passw = check_password_hash(resultTecnico[4], data_user.user_passw)

      if check_passw:
        return {
          "status": 200,
          "message": "Access success",
          "tecnico": {"nome":resultTecnico[1], "id":resultTecnico[0]}
        }
      else:
        return{
            "status": 401,
            "message": "Access denied"
          }
    else:
      return {"status": HTTP_401_UNAUTHORIZED, "message": "Access denied"}

    


@user_router.put("/update_user/{user_id}", response_model=UserSchema)
def update_user(data_update: UserSchema, user_id: str):
  with engine.connect() as conn:
    encryp_passw = generate_password_hash(data_update.user_passw, "pbkdf2:sha256:30", 30)

    conn.execute(users.update().values(nome=data_update.nome, username=data_update.username, user_passw=encryp_passw).where(users.c.id == user_id))

    result = conn.execute(users.select().where(users.c.id == user_id)).first()

    return result


@user_router.post("/update_image/", response_model=UserSchema)
def update_user(data_update: DataUserImg, user_id: str):
  with engine.connect() as conn:
    conn.execute(users.update().values(img_perfil=data_update.img_perfil).where(users.c.id == user_id))

    result = conn.execute(users.select().where(users.c.id == user_id)).first()

    return result



@user_router.post("/update_image_tecnico/", response_model=DataTecnicoImg)
def update_user(data_update: DataTecnicoImg, user_id: str):
  with engine.connect() as conn:
    conn.execute(tecnicos.update().values(img_perfil=data_update.img_perfil).where(tecnicos.c.id == user_id))

    result = conn.execute(tecnicos.select().where(tecnicos.c.id == user_id)).first()

    return result



@user_router.delete("/deleta_user/{user_id}", status_code=HTTP_204_NO_CONTENT)
def delete_user(user_id: str):
  with engine.connect() as conn:
    conn.execute(users.delete().where(users.c.id == user_id))

    return Response(status_code=HTTP_204_NO_CONTENT)



#Retorna todos os tecnicos
@user_router.get("/retorna_tecnicos")
def get_tecnicos():
  with engine.connect() as conn:
    result = conn.execute(tecnicos.select()).fetchall() 

    return result