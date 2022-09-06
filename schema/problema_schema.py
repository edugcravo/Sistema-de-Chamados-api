from pydantic import BaseModel
from typing import Optional

class ProblemaSchema(BaseModel):
  id: Optional[str]
  tipo_problema: str


