from sqlalchemy import Column, Integer, String


class Usuario:
    __tablename__ = 'usuario'

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String)
    senha = Column(String)
