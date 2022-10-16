from datetime import datetime
from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String, DateTime
from config.db import engine, meta_data

logs = Table("logs", meta_data, 
              Column("id", Integer, primary_key=True),
              Column("date", String(255), nullable=False),
              Column("tipo", String(255), nullable=False),
              Column("acao", String(255), nullable=False),
              Column("object_id", Integer, nullable=False))
              


meta_data.create_all(engine)

