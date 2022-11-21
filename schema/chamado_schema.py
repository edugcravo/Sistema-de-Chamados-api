from datetime import datetime, date, time
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
  data_criacao: Optional[date]
  data_finalizacao: Optional[date]
  hora_criacao: Optional[time]
  hora_finalizacao: Optional[time]



class editaChamado(BaseModel):
  resolucao_problema: Optional[str]
  tipo_problema: Optional[str]
  status: str


class cancelaChamado(BaseModel):
  status: str
  data_finalizacao: Optional[date]
  hora_finalizacao: Optional[time]

class filtroChamado(BaseModel):
  problema: Optional[list]
  setor: Optional[list]