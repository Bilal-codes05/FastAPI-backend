from sqlalchemy import create_engine
#for mapping
from sqlalchemy.ext.declarative import declarative_base
# sessionmaker is used to create a session
from sqlalchemy.orm import sessionmaker




SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"

engine=create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread":False})


sessionlocal=sessionmaker(bind=engine, autoflush=False, autocommit=False)


Base=declarative_base()
