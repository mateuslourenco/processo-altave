from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session
from starlette import status

from src.infra.providers import token_provider
from src.infra.sqlalchemy.config.database import get_db
from src.infra.sqlalchemy.repositorios.repositorio_usuario import RepositorioUsuario

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def obter_usuario_logado(token: str = Depends(oauth2_scheme), session: Session = Depends(get_db)):
    token_invalido = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token inválido')
    try:
        login = token_provider.verificar_access_token(token)
    except JWTError:
        raise token_invalido

    if not login:
        raise token_invalido

    usuario = RepositorioUsuario(session).obter_usuario(login)

    if not usuario:
        raise token_invalido

    return usuario
