from datetime import datetime
from pydantic import BaseModel
from typing import Optional



class DataChamado(BaseModel):
  id_equipamento: int
  local: str
  ramal: str
  tipo_problema: int
  desc_problema: str
  status: str
  id_tecnico: int
  id_usuario: int
  arquivo: str
  data_hora_criacao: Optional[datetime]


class editaChamado(BaseModel):
  resolucao_problema: Optional[str]
  tipo_problema: Optional[str]
  status: str


class cancelaChamado(BaseModel):
  status: str

class filtroChamado(BaseModel):
  problema: list
  setor: list[str]