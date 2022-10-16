from datetime import datetime
from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String, DateTime, Boolean
from config.db import engine, meta_data

acompanhamentos = Table("acompanhamentos", meta_data, 
              Column("id", Integer, primary_key=True),
              Column("id_chamado", String(255), nullable=False),
              Column("data", String(255), nullable=False),
              Column("resposta", String(255), nullable=False),
              Column("tecnico", Boolean, nullable=False))
              


meta_data.create_all(engine)

