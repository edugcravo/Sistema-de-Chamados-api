from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String, Date
from config.db import engine, meta_data

users = Table("users", meta_data, 
              Column("id", Integer, primary_key=True),
              Column("nome", String(255), nullable=False),
              Column("username", String(255), nullable=False),
              Column("email", String(255), nullable=False),
              Column("nascimento", String(10), nullable=False),
              Column("setor", String(255), nullable=False),
              Column("ramal", String(255), nullable=False),
              Column("user_passw", String(255), nullable=False),
              Column("nivel", String(20), nullable=False))


meta_data.create_all(engine)