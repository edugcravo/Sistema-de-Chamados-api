from pydantic import BaseModel
from typing import Optional

class TecnicoSchema(BaseModel):
  # id: Optional[str]
  username: str
  nome: str
  especialidade: str
  user_passw: str
  qtd_chamado: Optional[int]


class DataTecnicoImg(BaseModel):
  img_perfil: str