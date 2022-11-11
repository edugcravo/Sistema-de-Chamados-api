from datetime import datetime
from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String, DateTime
from config.db import engine, meta_data

problemas = Table("problemas", meta_data, 
              Column("id", Integer, primary_key=True),
              Column("tipo_problema", String(30), nullable=False),)
              


meta_data.create_all(engine)