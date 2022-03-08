from sqlalchemy import select
from sqlalchemy.orm import Session

from src.infra.sqlalchemy.models import models
from src.schemas import schemas


class RepositorioUsuario:

    """
    Repositorio que faz a comunicacao com o bando de dados
    """

    def __init__(self, session: Session):
        self.session = session

    def criar_usuario(self, usuario: schemas.Usuario):
        db_usuario = models.User(login=usuario.login,
                                 senha=usuario.senha
                                 )
        self.session.add(db_usuario)
        self.session.commit()
        self.session.refresh(db_usuario)
        return db_usuario

    def obter_usuario(self, login):
        query = select(models.User).where(models.User.login == login)
        return self.session.execute(query).scalars().first()
