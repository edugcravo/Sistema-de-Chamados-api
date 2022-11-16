from datetime import datetime
from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String, DateTime
from config.db import engine, meta_data

tecnicos = Table("tecnicos", meta_data, 
              Column("id", Integer, primary_key=True),
              Column("username", String(255), nullable=False),
              Column("nome", String(255), nullable=False),
              Column("especialidade", String(255), nullable=False),
              Column("user_passw", String(255), nullable=False),
              Column("img_perfil", String(255), nullable=False),
              Column("qtd_chamado", Integer, nullable=False))
              


meta_data.create_all(engine)