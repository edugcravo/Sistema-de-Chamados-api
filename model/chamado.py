from datetime import datetime

from sqlalchemy import Column, Table
from sqlalchemy.sql.sqltypes import DateTime, Integer, String, VARCHAR, Date, Time

from config.db import engine, meta_data

chamados = Table("chamados", meta_data, 
              Column("id", Integer, primary_key=True),
              Column("id_equipamento", Integer, nullable=False),
              Column("local", String(255), nullable=False),
              Column("ramal", String(255), nullable=False),
              Column("tipo_problema", Integer, nullable=False),
              Column("desc_problema", String(255), nullable=False),
              Column("resolucao_problema", String(255), nullable=False),
              Column("status", String(25), nullable=False),
              Column("id_tecnico", Integer, nullable=False),
              Column("id_usuario", Integer, nullable=False),
              Column("arquivo",VARCHAR(255) , nullable=False),
              Column("data_criacao", Date, nullable=False),
              Column("data_finalizacao", Date, nullable=False),
              Column("hora_criacao", Time, nullable=False),
              Column("hora_finalizacao", Time, nullable=False))
              


meta_data.create_all(engine)