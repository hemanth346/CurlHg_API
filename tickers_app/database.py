import databases
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# DATABASE_URL = 'postgresql://{}:{}@{}:{}/{}?sslmode={}'.format(db_username,db_password, host_server, db_server_port, database_name, ssl_mode)
DATABASE_URL = 'postgresql://postgres:root@localhost:5432/postgres?sslmode=prefer'

database = databases.Database(DATABASE_URL)

engine = create_engine(DATABASE_URL)

# instances of below class will actual db session
SessionMaker = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# classes inherited from this will be ORM models i.e. DB tables
Base = declarative_base()
