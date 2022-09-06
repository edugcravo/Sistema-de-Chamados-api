from curses import meta
from sqlalchemy import create_engine, MetaData

engine = create_engine("mysql+pymysql://root:@localhost:3306/chamados")

meta_data = MetaData()