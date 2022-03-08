"""
Configuração do banco de dados conforme documentação do fast api
https://fastapi.tiangolo.com/tutorial/sql-databases/
"""
from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Utilizado python-decouple para extrair vairavel de ambiente DATABASE_URL
db_url = config('DATABASE_URL', default='sqlite:///./altave.db')


# Atualizado db_url para ser compativel com sqlaqlchemy
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

SQLALCHEMY_DATABASE_URL = db_url

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def criar_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
