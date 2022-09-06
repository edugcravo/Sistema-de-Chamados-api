from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
  # id: Optional[str]
  nome: str
  username: str
  email: str
  nascimento: str
  setor: str
  ramal: int
  user_passw: str
  nivel: str


class DataUser(BaseModel):
  username: str
  user_passw: str