from datetime import datetime
from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String, DateTime
from config.db import engine, meta_data

chamados = Table("chamados", meta_data, 
              Column("id", Integer, primary_key=True),
              Column("id_equipamento", Integer, nullable=False),
              Column("local", String(255), nullable=False),
              Column("ramal", String(255), nullable=False),
              Column("tipo_problema", String(255), nullable=False),
              Column("desc_problema", String(255), nullable=False),
              Column("resolucao_problema", String(255), nullable=False),
              Column("status", String(25), nullable=False),
              Column("id_tecnico", String(255), nullable=False),
              Column("id_usuario", String(255), nullable=False),
              Column("data_hora_criacao", DateTime, nullable=False),)
              


meta_data.create_all(engine)